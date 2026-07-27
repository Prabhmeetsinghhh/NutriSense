import { useState } from "react";
import {
  Card,
  Typography,
  Box,
  Stack,
  Button,
  Chip,
  Rating,
  TextField,
  Collapse,
  IconButton,
  Paper,
} from "@mui/material";
import {
  ExpandMore as ExpandMoreIcon,
  PlayCircle as PlayCircleIcon,
} from "@mui/icons-material";
import axios from "../api/axiosInstance";

interface ExerciseData {
  id: string;
  name: string;
  muscle_group: string;
  difficulty: "beginner" | "intermediate" | "advanced";
  sets_reps: string;
  video_url: string;
  form_tips: string[];
  calories_per_set: number;
  description: string;
  equipment: string;
}

interface ExerciseVideoCardProps {
  exercise: ExerciseData;
  isDark: boolean;
  email: string;
  onPreferenceSaved?: () => void;
}

const ExerciseVideoCard = ({
  exercise,
  isDark,
  email,
  onPreferenceSaved,
}: ExerciseVideoCardProps) => {
  const [expanded, setExpanded] = useState(false);
  const [rating, setRating] = useState<number | null>(null);
  const [notes, setNotes] = useState("");
  const [difficulty, setDifficulty] = useState("moderate");
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [showVideo, setShowVideo] = useState(false);
  const [videoLoadFailed, setVideoLoadFailed] = useState(false);

  const accentColor = isDark ? "#D4AF37" : "#2B5F3A";

  const getYouTubeVideoId = (url: string): string | null => {
    if (!url) {
      return null;
    }

    try {
      const parsed = new URL(url);
      const host = parsed.hostname.replace(/^www\./, "").toLowerCase();
      if (host.includes("youtube.com")) {
        const direct = parsed.searchParams.get("v");
        if (direct) {
          return direct;
        }
        const pathParts = parsed.pathname.split("/").filter(Boolean);
        const embedIdx = pathParts.findIndex((part) => part === "embed" || part === "shorts");
        if (embedIdx >= 0 && pathParts[embedIdx + 1]) {
          return pathParts[embedIdx + 1];
        }
      }
      if (host.includes("youtu.be")) {
        const pathId = parsed.pathname.split("/").filter(Boolean)[0];
        if (pathId) {
          return pathId;
        }
      }
    } catch {
      // Fall back to regex extraction for partially formed URLs.
    }

    const patterns = [
      /youtube\.com\/embed\/([A-Za-z0-9_-]{6,})/,
      /youtube\.com\/watch\?v=([A-Za-z0-9_-]{6,})/,
      /youtu\.be\/([A-Za-z0-9_-]{6,})/,
      /youtube\.com\/shorts\/([A-Za-z0-9_-]{6,})/,
    ];

    for (const pattern of patterns) {
      const match = url.match(pattern);
      if (match?.[1]) {
        return match[1];
      }
    }

    return null;
  };

  const getWatchUrl = (url: string): string => {
    const videoId = getYouTubeVideoId(url);
    if (videoId) {
      return `https://www.youtube.com/watch?v=${videoId}`;
    }
    if (url) {
      return url;
    }
    const query = encodeURIComponent(`${exercise.name} exercise proper form`);
    return `https://www.youtube.com/results?search_query=${query}`;
  };

  const getEmbedUrl = (url: string): string | null => {
    const videoId = getYouTubeVideoId(url);
    return videoId ? `https://www.youtube.com/embed/${videoId}?rel=0` : null;
  };

  const previewImage = (() => {
    const videoId = getYouTubeVideoId(exercise.video_url);
    return videoId ? `https://img.youtube.com/vi/${videoId}/hqdefault.jpg` : null;
  })();

  const handleSavePreference = async () => {
    if (!rating) {
      alert("Please select a rating");
      return;
    }

    setSaving(true);
    try {
      await axios.post(`/exercise-preferences/${email}`, {
        exercise_id: exercise.id,
        rating: rating,
        notes: notes,
        difficulty_rating: difficulty,
      });

      setSaved(true);
      setTimeout(() => {
        setRating(null);
        setNotes("");
        setDifficulty("moderate");
        setSaved(false);
      }, 2000);

      onPreferenceSaved?.();
    } catch (error) {
      console.error("Error saving preference:", error);
      alert("Failed to save preference");
    } finally {
      setSaving(false);
    }
  };

  const openVideo = () => {
    const fallbackSearch = `https://www.youtube.com/results?search_query=${encodeURIComponent(`${exercise.name} exercise proper form`)}`;
    const target = videoLoadFailed ? fallbackSearch : getWatchUrl(exercise.video_url);
    window.open(target, "_blank", "noopener,noreferrer");
  };

  const embedUrl = getEmbedUrl(exercise.video_url);

  const difficultyColor = {
    beginner: "#4CAF50",
    intermediate: "#FFC107",
    advanced: "#F44336",
  };

  return (
    <Card
      sx={{
        borderRadius: "14px",
        background: isDark ? "rgba(255,255,255,0.06)" : "rgba(0, 0, 0, 0.03)",
        border: isDark ? "1px solid rgba(212,175,55,0.24)" : "1px solid rgba(43, 95, 58, 0.15)",
        color: isDark ? "#f8f6f0" : "#1A1A1A",
        transition: "all 0.3s ease",
        overflow: "hidden",
      }}
    >
      <Box sx={{ p: 2 }}>
        <Stack direction="row" justifyContent="space-between" alignItems="start" sx={{ mb: 1.2 }}>
          <Box>
            <Typography sx={{ fontWeight: 700, fontSize: "1.1rem", mb: 0.4 }}>
              {exercise.name}
            </Typography>
            <Stack direction="row" spacing={0.8} sx={{ mb: 1 }}>
              <Chip
                label={exercise.difficulty}
                size="small"
                sx={{
                  background: difficultyColor[exercise.difficulty],
                  color: "#fff",
                  fontWeight: 600,
                }}
              />
              <Chip
                label={exercise.muscle_group}
                size="small"
                sx={{
                  background: isDark ? "rgba(212,175,55,0.2)" : "rgba(43, 95, 58, 0.1)",
                  color: accentColor,
                  fontWeight: 600,
                }}
              />
            </Stack>
          </Box>
          <IconButton
            onClick={() => setExpanded(!expanded)}
            sx={{
              transform: expanded ? "rotate(180deg)" : "rotate(0deg)",
              transition: "transform 0.3s ease",
            }}
          >
            <ExpandMoreIcon sx={{ color: accentColor }} />
          </IconButton>
        </Stack>

        <Typography sx={{ fontSize: "0.9rem", color: isDark ? "rgba(248,246,240,0.8)" : "rgba(0, 0, 0, 0.75)", mb: 1 }}>
          {exercise.description}
        </Typography>

        {/* VIDEO PREVIEW */}
        <Box
          sx={{
            position: "relative",
            paddingBottom: "56.25%",
            height: 0,
            overflow: "hidden",
            borderRadius: "10px",
            mb: 1.4,
            background: "#000",
          }}
        >
          {!showVideo && previewImage && !videoLoadFailed ? (
            <Box
              component="button"
              onClick={() => setShowVideo(true)}
              sx={{
                position: "absolute",
                inset: 0,
                width: "100%",
                height: "100%",
                p: 0,
                border: "none",
                cursor: "pointer",
                background: "transparent",
                overflow: "hidden",
              }}
            >
              <Box
                component="img"
                src={previewImage}
                alt={`${exercise.name} preview`}
                sx={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                  display: "block",
                }}
                onError={() => setVideoLoadFailed(true)}
              />
              <Box
                sx={{
                  position: "absolute",
                  inset: 0,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  background: "linear-gradient(180deg, rgba(0,0,0,0.12), rgba(0,0,0,0.5))",
                }}
              >
                <Box
                  sx={{
                    width: 74,
                    height: 74,
                    borderRadius: "50%",
                    display: "grid",
                    placeItems: "center",
                    background: "rgba(0,0,0,0.55)",
                    border: "1px solid rgba(255,255,255,0.28)",
                    color: "#fff",
                  }}
                >
                  <PlayCircleIcon sx={{ fontSize: 54 }} />
                </Box>
              </Box>
            </Box>
          ) : showVideo && !videoLoadFailed && embedUrl ? (
            <iframe
              src={embedUrl}
              title={exercise.name}
              style={{
                position: "absolute",
                top: 0,
                left: 0,
                width: "100%",
                height: "100%",
                border: "none",
                borderRadius: "10px",
              }}
              allowFullScreen
              onError={() => setVideoLoadFailed(true)}
            />
          ) : (
            <Box
              sx={{
                position: "absolute",
                inset: 0,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                gap: 1,
                textAlign: "center",
                px: 2,
                background: "linear-gradient(135deg, rgba(0,0,0,0.9), rgba(43,95,58,0.85))",
                color: "#fff",
              }}
            >
              <PlayCircleIcon sx={{ fontSize: 56, color: accentColor }} />
              <Typography sx={{ fontWeight: 700 }}>Video preview unavailable</Typography>
              <Typography sx={{ fontSize: "0.85rem", opacity: 0.88 }}>
                Open the exercise in a new tab if the embedded player does not load on your device.
              </Typography>
              <Button
                variant="contained"
                onClick={openVideo}
                sx={{
                  mt: 0.5,
                  background: accentColor,
                  color: isDark ? "#111" : "#fff",
                  fontWeight: 700,
                }}
              >
                Open Video
              </Button>
            </Box>
          )}
        </Box>

        <Stack direction={{ xs: "column", sm: "row" }} spacing={0.8} sx={{ mb: 1.2 }}>
          <Button
            size="small"
            variant="outlined"
            onClick={() => {
              setVideoLoadFailed(false);
              setShowVideo((current) => !current);
            }}
            startIcon={<PlayCircleIcon />}
            sx={{ textTransform: "none" }}
          >
            {showVideo ? "Hide Player" : "Play Video"}
          </Button>
          <Button
            size="small"
            variant="outlined"
            onClick={openVideo}
            sx={{ textTransform: "none" }}
          >
            Open in New Tab
          </Button>
        </Stack>

        <Stack direction="row" spacing={0.8} sx={{ mb: 1.2, flexWrap: "wrap" }}>
          <Chip label={`${exercise.sets_reps}`} size="small" variant="outlined" />
          <Chip label={`${exercise.calories_per_set} cal/set`} size="small" variant="outlined" />
          <Chip label={exercise.equipment} size="small" variant="outlined" />
        </Stack>

        <Collapse in={expanded} timeout="auto">
          <Box sx={{ mt: 1.4, pt: 1.4, borderTop: isDark ? "1px solid rgba(212,175,55,0.24)" : "1px solid rgba(43, 95, 58, 0.15)" }}>
            {/* FORM TIPS */}
            <Typography sx={{ fontWeight: 700, mb: 0.8, color: accentColor, fontSize: "0.95rem" }}>
              ✓ Form Tips for Beginners
            </Typography>
            <Stack spacing={0.6} sx={{ mb: 1.4 }}>
              {exercise.form_tips.map((tip, idx) => (
                <Typography
                  key={idx}
                  sx={{
                    fontSize: "0.88rem",
                    color: isDark ? "rgba(248,246,240,0.85)" : "rgba(0, 0, 0, 0.8)",
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  <Box
                    sx={{
                      display: "inline-block",
                      width: "6px",
                      height: "6px",
                      borderRadius: "50%",
                      background: accentColor,
                      mr: 1,
                    }}
                  />
                  {tip}
                </Typography>
              ))}
            </Stack>

            {/* PREFERENCE RATING */}
            <Paper
              sx={{
                p: 1.4,
                background: isDark ? "rgba(212,175,55,0.1)" : "rgba(43, 95, 58, 0.08)",
                borderRadius: "10px",
                border: isDark ? "1px solid rgba(212,175,55,0.2)" : "1px solid rgba(43, 95, 58, 0.1)",
              }}
            >
              <Typography sx={{ fontWeight: 700, mb: 1, fontSize: "0.95rem", color: accentColor }}>
                Rate This Exercise
              </Typography>

              <Stack spacing={1}>
                <Box>
                  <Typography sx={{ fontSize: "0.85rem", mb: 0.5, color: isDark ? "rgba(248,246,240,0.8)" : "rgba(0, 0, 0, 0.75)" }}>
                    How much do you like this?
                  </Typography>
                  <Rating
                    value={rating}
                    onChange={(_, newValue) => setRating(newValue)}
                    size="large"
                    sx={{ color: accentColor }}
                  />
                </Box>

                <TextField
                  label="Notes (optional)"
                  multiline
                  rows={2}
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="E.g., Love this! Easy to do at home"
                  size="small"
                  sx={{
                    "& .MuiOutlinedInput-root": {
                      color: isDark ? "#f8f6f0" : "#1A1A1A",
                      background: isDark ? "rgba(255,255,255,0.04)" : "rgba(0, 0, 0, 0.02)",
                    },
                    "& .MuiOutlinedInput-notchedOutline": {
                      borderColor: isDark ? "rgba(212,175,55,0.2)" : "rgba(43, 95, 58, 0.1)",
                    },
                  }}
                />

                <Box>
                  <Typography sx={{ fontSize: "0.85rem", mb: 0.5, color: isDark ? "rgba(248,246,240,0.8)" : "rgba(0, 0, 0, 0.75)" }}>
                    How difficult was it?
                  </Typography>
                  <Stack direction="row" spacing={0.8}>
                    {["easy", "moderate", "hard"].map((d) => (
                      <Button
                        key={d}
                        variant={difficulty === d ? "contained" : "outlined"}
                        size="small"
                        onClick={() => setDifficulty(d)}
                        sx={{
                          textTransform: "capitalize",
                          background: difficulty === d ? accentColor : "transparent",
                          color: difficulty === d ? (isDark ? "#111" : "#fff") : accentColor,
                        }}
                      >
                        {d}
                      </Button>
                    ))}
                  </Stack>
                </Box>

                <Button
                  variant="contained"
                  onClick={handleSavePreference}
                  disabled={saving || !rating}
                  sx={{
                    background: accentColor,
                    color: isDark ? "#111" : "#fff",
                    fontWeight: 700,
                  }}
                >
                  {saving ? "Saving..." : saved ? "✓ Saved!" : "Save Preference"}
                </Button>
              </Stack>
            </Paper>
          </Box>
        </Collapse>
      </Box>
    </Card>
  );
};

export default ExerciseVideoCard;
