import { useEffect, useMemo, useState } from "react";
import {
  Alert,
  Avatar,
  Box,
  Button,
  Card,
  CircularProgress,
  Divider,
  Paper,
  Stack,
  TextField,
  Typography,
  Chip,
} from "@mui/material";
import AutoAwesomeRoundedIcon from "@mui/icons-material/AutoAwesomeRounded";
import SendRoundedIcon from "@mui/icons-material/SendRounded";
import SmartToyRoundedIcon from "@mui/icons-material/SmartToyRounded";
import PersonRoundedIcon from "@mui/icons-material/PersonRounded";
import axios from "../api/axiosInstance";

type CoachMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  created_at?: string;
};

type CoachSummary = {
  goal?: string;
  calories?: number;
  protein?: number;
  carbs?: number;
  fats?: number;
  meal_plan_summary?: string;
  workout_days?: string[];
  current_weight?: number;
  target_weight?: number;
  weight_gap?: number;
  reminder_suggestion?: string;
  starter_prompt?: string;
};

type CoachStrategy = {
  goal?: string;
  current_weight?: number;
  target_weight?: number;
  calorie_target?: number;
  protein_target?: number;
  weekly_focus?: string[];
  meal_rules?: string[];
  workout_rules?: string[];
  check_in?: string;
};

type PersonalCoachPanelProps = {
  email: string;
  userProfile: Record<string, unknown>;
  currentPlan?: Record<string, unknown> | null;
  isDark: boolean;
};

const starterPrompts = [
  "What should I eat today?",
  "How do I get more protein cheaply?",
  "What should I do before my workout?",
  "How do I speed up fat loss safely?",
];

const PersonalCoachPanel = ({ email, userProfile, currentPlan, isDark }: PersonalCoachPanelProps) => {
  const [messages, setMessages] = useState<CoachMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [quickActions, setQuickActions] = useState<string[]>(starterPrompts);
  const [summary, setSummary] = useState<CoachSummary | null>(null);
  const [strategy, setStrategy] = useState<CoachStrategy | null>(null);

  const accentColor = isDark ? "#D4AF37" : "#2B5F3A";

  const pinnedPrompt = useMemo(() => {
    const target = Number(userProfile.target_weight ?? userProfile.targetWeight ?? 0);
    const current = Number(userProfile.weight ?? 0);
    const goal = String(userProfile.goal ?? "maintenance").replace(/_/g, " ");

    if (target > 0 && current > 0 && target !== current) {
      const direction = target < current ? "fat loss" : "muscle gain";
      return `I am ${current} kg and want to get to ${target} kg. Build me a ${direction} plan with meals, workouts, and weekly check-ins.`;
    }

    if (goal !== "maintenance") {
      return `Make me a ${goal} plan with budget-friendly meals and a workout strategy that matches my current routine.`;
    }

    return "Help me turn my saved plan into a daily meal and workout routine I can actually follow.";
  }, [userProfile]);

  const headerText = useMemo(() => {
    if (summary?.goal) {
      return `Your coach is tuned for ${summary.goal.replace(/_/g, " ")}.`;
    }
    return "Ask about meals, calories, workouts, recovery, or swaps.";
  }, [summary?.goal]);

  useEffect(() => {
    const fetchHistory = async () => {
      if (!email) return;

      setLoading(true);
      setError(null);
      try {
        const response = await axios.get(`/ml/personal-coach/${email}/history?limit=12`);
        if (response.data.status === "success") {
          const loaded = (response.data.messages ?? []).map((item: any) => ({
            id: item.id,
            role: item.role,
            content: item.content,
            created_at: item.created_at,
          }));
          setMessages(loaded.length > 0 ? loaded : [
            {
              id: "welcome",
              role: "assistant",
              content: "I’m your NutriSense coach. Ask me what to eat, how to adjust your calories, or what to do around workouts.",
            },
          ]);
        }
      } catch (err) {
        console.error("Error loading coach history:", err);
        setMessages([
          {
            id: "welcome",
            role: "assistant",
            content: "I’m your NutriSense coach. Ask me what to eat, how to adjust your calories, or what to do around workouts.",
          },
        ]);
      } finally {
        setLoading(false);
      }
    };

    void fetchHistory();
  }, [email]);

  const sendMessage = async (messageText?: string) => {
    const finalMessage = (messageText ?? input).trim();
    if (!finalMessage || !email || sending) {
      return;
    }

    const userMessage: CoachMessage = {
      id: `${Date.now()}-user`,
      role: "user",
      content: finalMessage,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setSending(true);
    setError(null);

    try {
      const response = await axios.post(`/ml/personal-coach/${email}`, {
        message: finalMessage,
        user_profile: userProfile,
        current_plan: currentPlan,
      });

      if (response.data.status === "success") {
        const assistantMessage: CoachMessage = {
          id: response.data.email ? `${Date.now()}-assistant` : `${Date.now()}-assistant-fallback`,
          role: "assistant",
          content: response.data.assistant_message || "I’ve noted that and updated your guidance.",
        };

        setMessages((prev) => [...prev, assistantMessage]);
        setQuickActions(response.data.quick_actions?.length ? response.data.quick_actions : starterPrompts);
        setSummary(response.data.coach_summary || null);
        setStrategy(response.data.coach_strategy || null);
      } else {
        setError("Coach could not process that request.");
      }
    } catch (err) {
      console.error("Coach request failed:", err);
      setError("Could not reach the coach right now. Try again in a moment.");
    } finally {
      setSending(false);
    }
  };

  return (
    <Stack spacing={1.6}>
      <Card
        sx={{
          p: 2.2,
          borderRadius: 3,
          background: isDark ? "rgba(255,255,255,0.06)" : "rgba(0,0,0,0.03)",
          border: isDark ? "1px solid rgba(212,175,55,0.24)" : "1px solid rgba(43,95,58,0.15)",
        }}
      >
        <Stack direction={{ xs: "column", sm: "row" }} spacing={1.4} alignItems={{ xs: "flex-start", sm: "center" }} justifyContent="space-between">
          <Box>
            <Stack direction="row" spacing={1} alignItems="center">
              <SmartToyRoundedIcon sx={{ color: accentColor }} />
              <Typography sx={{ fontWeight: 800, fontSize: "1.05rem" }}>Personal Coach</Typography>
            </Stack>
            <Typography sx={{ mt: 0.6, color: isDark ? "rgba(248,246,240,0.78)" : "rgba(0,0,0,0.68)" }}>
              {headerText}
            </Typography>
          </Box>

          {summary && (
            <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
              <Chip label={`${summary.calories ?? 0} kcal`} sx={{ background: isDark ? "rgba(212,175,55,0.16)" : "rgba(43,95,58,0.12)", color: isDark ? "#f8f6f0" : "#1A1A1A" }} />
              <Chip label={`${summary.protein ?? 0}g protein`} sx={{ background: isDark ? "rgba(212,175,55,0.16)" : "rgba(43,95,58,0.12)", color: isDark ? "#f8f6f0" : "#1A1A1A" }} />
            </Stack>
          )}
        </Stack>
      </Card>

      <Paper
        sx={{
          p: 2,
          borderRadius: 3,
          background: isDark ? "rgba(255,255,255,0.05)" : "rgba(255,255,255,0.82)",
          border: isDark ? "1px solid rgba(212,175,55,0.18)" : "1px solid rgba(43,95,58,0.12)",
        }}
      >
        <Typography sx={{ fontWeight: 700, mb: 0.8, color: accentColor }}>Pinned Starter</Typography>
        <Typography sx={{ color: isDark ? "rgba(248,246,240,0.8)" : "rgba(0,0,0,0.72)", mb: 1 }}>
          Start here if you want the coach to adapt to your personal goal.
        </Typography>
        <Button
          variant="outlined"
          startIcon={<AutoAwesomeRoundedIcon />}
          onClick={() => void sendMessage(pinnedPrompt)}
          sx={{
            textTransform: "none",
            borderRadius: 999,
            borderColor: accentColor,
            color: accentColor,
          }}
        >
          {pinnedPrompt}
        </Button>
      </Paper>

      <Paper
        sx={{
          p: 2,
          borderRadius: 3,
          background: isDark ? "rgba(255,255,255,0.05)" : "rgba(255,255,255,0.82)",
          border: isDark ? "1px solid rgba(212,175,55,0.18)" : "1px solid rgba(43,95,58,0.12)",
        }}
      >
        <Typography sx={{ fontWeight: 700, mb: 0.8, color: accentColor }}>Quick Prompts</Typography>
        <Stack direction="row" flexWrap="wrap" useFlexGap spacing={1}>
          {quickActions.map((prompt) => (
            <Button
              key={prompt}
              size="small"
              variant="outlined"
              startIcon={<AutoAwesomeRoundedIcon />}
              onClick={() => void sendMessage(prompt)}
              sx={{
                textTransform: "none",
                borderRadius: 999,
                borderColor: accentColor,
                color: accentColor,
              }}
            >
              {prompt}
            </Button>
          ))}
        </Stack>
      </Paper>

      {strategy && (
        <Paper
          sx={{
            p: 2,
            borderRadius: 3,
            background: isDark ? "rgba(255,255,255,0.05)" : "rgba(255,255,255,0.82)",
            border: isDark ? "1px solid rgba(212,175,55,0.18)" : "1px solid rgba(43,95,58,0.12)",
          }}
        >
          <Typography sx={{ fontWeight: 700, mb: 1, color: accentColor }}>Your Strategy</Typography>
          <Stack spacing={0.8}>
            <Typography sx={{ color: isDark ? "rgba(248,246,240,0.82)" : "rgba(0,0,0,0.75)" }}>
              <strong>Calories:</strong> {strategy.calorie_target ?? summary?.calories ?? 0} kcal | <strong>Protein:</strong> {strategy.protein_target ?? summary?.protein ?? 0}g
            </Typography>
            {strategy.weekly_focus?.length ? (
              <Typography sx={{ color: isDark ? "rgba(248,246,240,0.82)" : "rgba(0,0,0,0.75)" }}>
                <strong>Weekly focus:</strong> {strategy.weekly_focus.join(" · ")}
              </Typography>
            ) : null}
            {strategy.meal_rules?.length ? (
              <Typography sx={{ color: isDark ? "rgba(248,246,240,0.82)" : "rgba(0,0,0,0.75)" }}>
                <strong>Meal rules:</strong> {strategy.meal_rules.join(" · ")}
              </Typography>
            ) : null}
            {strategy.workout_rules?.length ? (
              <Typography sx={{ color: isDark ? "rgba(248,246,240,0.82)" : "rgba(0,0,0,0.75)" }}>
                <strong>Workout rules:</strong> {strategy.workout_rules.join(" · ")}
              </Typography>
            ) : null}
            {(strategy.check_in || summary?.reminder_suggestion) && (
              <Typography sx={{ color: isDark ? "rgba(248,246,240,0.82)" : "rgba(0,0,0,0.75)" }}>
                <strong>Next check-in:</strong> {strategy.check_in || summary?.reminder_suggestion}
              </Typography>
            )}
          </Stack>
        </Paper>
      )}

      <Card
        sx={{
          p: 2,
          borderRadius: 3,
          background: isDark ? "rgba(255,255,255,0.05)" : "rgba(0,0,0,0.03)",
          border: isDark ? "1px solid rgba(212,175,55,0.18)" : "1px solid rgba(43,95,58,0.12)",
        }}
      >
        <Stack spacing={1.3} sx={{ maxHeight: 560, overflowY: "auto", pr: 0.5 }}>
          {loading ? (
            <Box sx={{ display: "grid", placeItems: "center", minHeight: 180 }}>
              <CircularProgress sx={{ color: accentColor }} />
            </Box>
          ) : (
            messages.map((message) => (
              <Stack
                key={message.id}
                direction="row"
                spacing={1}
                justifyContent={message.role === "user" ? "flex-end" : "flex-start"}
                alignItems="flex-start"
              >
                {message.role === "assistant" && (
                  <Avatar sx={{ bgcolor: accentColor, width: 32, height: 32 }}>
                    <SmartToyRoundedIcon sx={{ fontSize: 18 }} />
                  </Avatar>
                )}
                <Box
                  sx={{
                    maxWidth: { xs: "88%", sm: "78%" },
                    p: 1.4,
                    borderRadius: 3,
                    background: message.role === "user"
                      ? isDark
                        ? "rgba(212,175,55,0.16)"
                        : "rgba(43,95,58,0.12)"
                      : isDark
                      ? "rgba(255,255,255,0.08)"
                      : "rgba(255,255,255,0.92)",
                    border: isDark
                      ? "1px solid rgba(212,175,55,0.18)"
                      : "1px solid rgba(43,95,58,0.12)",
                  }}
                >
                  <Stack direction="row" spacing={0.75} alignItems="center" sx={{ mb: 0.5 }}>
                    {message.role === "user" ? <PersonRoundedIcon sx={{ fontSize: 16 }} /> : <SmartToyRoundedIcon sx={{ fontSize: 16, color: accentColor }} />}
                    <Typography sx={{ fontSize: "0.78rem", fontWeight: 700, color: isDark ? "rgba(248,246,240,0.7)" : "rgba(0,0,0,0.64)" }}>
                      {message.role === "user" ? "You" : "Coach"}
                    </Typography>
                  </Stack>
                  <Typography sx={{ whiteSpace: "pre-wrap", color: isDark ? "#F8F6F0" : "#1A1A1A" }}>
                    {message.content}
                  </Typography>
                </Box>
              </Stack>
            ))
          )}
        </Stack>

        {(summary?.meal_plan_summary || summary?.starter_prompt) && (
          <Box sx={{ mt: 1.6, p: 1.6, borderRadius: 2, background: isDark ? "rgba(212,175,55,0.08)" : "rgba(43,95,58,0.06)" }}>
            <Typography sx={{ fontSize: "0.82rem", fontWeight: 700, color: accentColor, mb: 0.5 }}>Meal plan snapshot</Typography>
            <Typography sx={{ fontSize: "0.88rem", color: isDark ? "rgba(248,246,240,0.8)" : "rgba(0,0,0,0.72)" }}>
              {summary.meal_plan_summary || summary.starter_prompt}
            </Typography>
          </Box>
        )}

        {error && (
          <Alert severity="error" sx={{ mt: 1.5 }}>
            {error}
          </Alert>
        )}

        <Divider sx={{ my: 1.5 }} />

        <Stack direction={{ xs: "column", sm: "row" }} spacing={1} alignItems="flex-end">
          <TextField
            fullWidth
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Ask about meals, calories, or workouts..."
            multiline
            minRows={2}
            sx={{
              "& .MuiOutlinedInput-root": {
                color: isDark ? "#F8F6F0" : "#1A1A1A",
                background: isDark ? "rgba(255,255,255,0.04)" : "rgba(255,255,255,0.9)",
              },
            }}
          />
          <Button
            variant="contained"
            onClick={() => void sendMessage()}
            disabled={sending || !input.trim()}
            endIcon={sending ? <CircularProgress size={16} sx={{ color: "inherit" }} /> : <SendRoundedIcon />}
            sx={{
              minWidth: { xs: "100%", sm: 150 },
              textTransform: "none",
              borderRadius: 999,
              backgroundColor: accentColor,
              color: isDark ? "#111" : "#fff",
              py: 1.2,
              "&:hover": { backgroundColor: isDark ? "#E8C969" : "#214C2E" },
            }}
          >
            Send
          </Button>
        </Stack>
      </Card>
    </Stack>
  );
};

export default PersonalCoachPanel;