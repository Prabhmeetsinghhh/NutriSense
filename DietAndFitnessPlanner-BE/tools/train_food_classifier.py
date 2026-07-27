import json
import os
import sys
from datetime import datetime

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)


def main() -> None:
    try:
        import tensorflow as tf
    except Exception as exc:
        raise RuntimeError("TensorFlow is required for food image model training") from exc

    dataset_dir = os.path.join(PROJECT_ROOT, "data", "food_images")
    model_dir = os.path.join(PROJECT_ROOT, "models")
    os.makedirs(model_dir, exist_ok=True)

    if not os.path.exists(dataset_dir):
        raise FileNotFoundError(
            f"Dataset folder not found: {dataset_dir}. "
            "Create class folders inside data/food_images (one folder per food class)."
        )

    image_size = (224, 224)
    batch_size = 32
    seed = 42

    train_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_dir,
        validation_split=0.2,
        subset="training",
        seed=seed,
        image_size=image_size,
        batch_size=batch_size,
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_dir,
        validation_split=0.2,
        subset="validation",
        seed=seed,
        image_size=image_size,
        batch_size=batch_size,
    )

    class_names = train_ds.class_names

    autotune = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=autotune)
    val_ds = val_ds.prefetch(buffer_size=autotune)

    base_model = tf.keras.applications.EfficientNetB0(
        include_top=False,
        weights="imagenet",
        input_shape=(224, 224, 3),
    )
    base_model.trainable = False

    data_augmentation = tf.keras.Sequential(
        [
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.08),
            tf.keras.layers.RandomZoom(0.1),
            tf.keras.layers.RandomContrast(0.1),
        ]
    )

    inputs = tf.keras.Input(shape=(224, 224, 3))
    x = data_augmentation(inputs)
    x = tf.keras.applications.efficientnet.preprocess_input(x)
    x = base_model(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.25)(x)
    outputs = tf.keras.layers.Dense(len(class_names), activation="softmax")(x)
    model = tf.keras.Model(inputs, outputs)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=4, restore_best_weights=True),
        tf.keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2),
    ]

    history = model.fit(train_ds, validation_data=val_ds, epochs=15, callbacks=callbacks)

    # Fine-tune top layers for better local-domain adaptation
    base_model.trainable = True
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    fine_history = model.fit(train_ds, validation_data=val_ds, epochs=8, callbacks=callbacks)

    metrics = model.evaluate(val_ds, return_dict=True)

    model_path = os.path.join(model_dir, "food_classifier.keras")
    labels_path = os.path.join(model_dir, "food_classifier.labels.json")
    metrics_path = os.path.join(model_dir, "food_classifier.metrics.json")

    model.save(model_path)
    with open(labels_path, "w", encoding="utf-8") as f:
        json.dump(class_names, f, indent=2, ensure_ascii=False)

    payload = {
        "metrics": metrics,
        "class_count": len(class_names),
        "class_names": class_names,
        "trained_at": datetime.utcnow().isoformat() + "Z",
        "epochs_stage_1": len(history.history.get("loss", [])),
        "epochs_stage_2": len(fine_history.history.get("loss", [])),
    }
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print("Food classifier trained successfully")
    print(f"model: {model_path}")
    print(f"labels: {labels_path}")
    print(f"metrics: {metrics_path}")


if __name__ == "__main__":
    main()
