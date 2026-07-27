import { useMemo, useState } from "react";
import {
  Badge,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Divider,
  Drawer,
  IconButton,
  Stack,
  Tooltip,
  Typography,
} from "@mui/material";
import NotificationsActiveRoundedIcon from "@mui/icons-material/NotificationsActiveRounded";
import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import DoneAllRoundedIcon from "@mui/icons-material/DoneAllRounded";
import OpenInNewRoundedIcon from "@mui/icons-material/OpenInNewRounded";
import { useNavigate } from "react-router-dom";
import { useTheme } from "../context/ThemeContext";
import { useNotifications } from "../context/NotificationContext";

const severityPalette = {
  success: { border: "rgba(76, 175, 80, 0.65)", background: "rgba(76, 175, 80, 0.12)" },
  warning: { border: "rgba(255, 193, 7, 0.72)", background: "rgba(255, 193, 7, 0.12)" },
  error: { border: "rgba(244, 67, 54, 0.72)", background: "rgba(244, 67, 54, 0.12)" },
  info: { border: "rgba(43, 95, 58, 0.55)", background: "rgba(43, 95, 58, 0.1)" },
} as const;

const NotificationCenter = () => {
  const navigate = useNavigate();
  const { theme } = useTheme();
  const { notifications, unreadCount, loading, markAsRead, markAllAsRead } = useNotifications();
  const [open, setOpen] = useState(false);

  const accentColor = theme === "dark" ? "#D4AF37" : "#2B5F3A";

  const sortedNotifications = useMemo(
    () => [...notifications].sort((left, right) => Number(Boolean(left.read)) - Number(Boolean(right.read))),
    [notifications]
  );

  const handleOpenPath = async (notificationId: string, path?: string | null) => {
    await markAsRead(notificationId);
    if (path) {
      navigate(path);
      setOpen(false);
    }
  };

  return (
    <>
      <Tooltip title={unreadCount > 0 ? `${unreadCount} new notification${unreadCount === 1 ? "" : "s"}` : "Notifications"}>
        <IconButton
          onClick={() => setOpen(true)}
          sx={{
            color: accentColor,
            backgroundColor: theme === "dark" ? "rgba(212, 175, 55, 0.12)" : "rgba(43, 95, 58, 0.1)",
            border: theme === "dark" ? "1px solid rgba(212,175,55,0.34)" : "1px solid rgba(43,95,58,0.22)",
            backdropFilter: "blur(6px)",
            boxShadow: theme === "dark" ? "0 8px 20px rgba(212,175,55,0.16)" : "0 8px 20px rgba(43,95,58,0.12)",
            borderRadius: "50%",
            width: 48,
            height: 48,
            transition: "all 0.3s ease",
            animation: unreadCount > 0 ? "notif-pulse 1.8s ease-in-out infinite" : "none",
            "@keyframes notif-pulse": {
              "0%, 100%": { transform: "scale(1)", boxShadow: theme === "dark" ? "0 8px 20px rgba(212,175,55,0.16)" : "0 8px 20px rgba(43,95,58,0.12)" },
              "50%": { transform: "scale(1.05)", boxShadow: theme === "dark" ? "0 12px 26px rgba(212,175,55,0.25)" : "0 12px 26px rgba(43,95,58,0.2)" },
            },
            "&:hover": {
              backgroundColor: theme === "dark" ? "rgba(212, 175, 55, 0.2)" : "rgba(43, 95, 58, 0.16)",
            },
          }}
        >
          <Badge color="error" badgeContent={unreadCount} overlap="circular">
            <NotificationsActiveRoundedIcon fontSize="medium" />
          </Badge>
        </IconButton>
      </Tooltip>

      <Drawer
        anchor="right"
        open={open}
        onClose={() => setOpen(false)}
        PaperProps={{
          sx: {
            width: { xs: "100%", sm: 420 },
            maxWidth: "100vw",
            background: theme === "dark"
              ? "linear-gradient(180deg, rgba(18,18,24,0.98) 0%, rgba(8,8,12,0.98) 100%)"
              : "linear-gradient(180deg, rgba(255,255,255,0.98) 0%, rgba(248,246,241,0.98) 100%)",
            color: theme === "dark" ? "#F8F6F0" : "#1A1A1A",
          },
        }}
      >
        <Box sx={{ p: 2.2, display: "flex", flexDirection: "column", height: "100%" }}>
          <Stack direction="row" alignItems="center" justifyContent="space-between" spacing={2} sx={{ mb: 1.5 }}>
            <Box>
              <Typography sx={{ fontSize: "1.15rem", fontWeight: 800 }}>Notifications</Typography>
              <Typography sx={{ fontSize: "0.88rem", color: theme === "dark" ? "rgba(248,246,240,0.72)" : "rgba(0,0,0,0.65)" }}>
                Quick prompts that keep users engaged
              </Typography>
            </Box>

            <Stack direction="row" spacing={0.5}>
              <Tooltip title="Mark all as read">
                <span>
                  <IconButton onClick={() => void markAllAsRead()} disabled={unreadCount === 0 || loading}>
                    <DoneAllRoundedIcon />
                  </IconButton>
                </span>
              </Tooltip>
              <IconButton onClick={() => setOpen(false)}>
                <CloseRoundedIcon />
              </IconButton>
            </Stack>
          </Stack>

          <Divider sx={{ mb: 2 }} />

          <Stack spacing={1.2} sx={{ flex: 1, overflowY: "auto", pr: 0.5 }}>
            {loading ? (
              <Box sx={{ display: "grid", placeItems: "center", minHeight: 180 }}>
                <CircularProgress size={28} sx={{ color: accentColor }} />
              </Box>
            ) : sortedNotifications.length === 0 ? (
              <PaperLike>
                <Typography sx={{ fontWeight: 700, mb: 0.6 }}>No notifications yet</Typography>
                <Typography sx={{ fontSize: "0.92rem", color: theme === "dark" ? "rgba(248,246,240,0.72)" : "rgba(0,0,0,0.65)" }}>
                  When you generate a plan or save workout feedback, the app will place it here.
                </Typography>
              </PaperLike>
            ) : (
              sortedNotifications.map((notification) => {
                const palette = severityPalette[notification.type as keyof typeof severityPalette] ?? severityPalette.info;
                return (
                  <Card
                    key={notification.id}
                    variant="outlined"
                    sx={{
                      borderColor: notification.read ? "transparent" : palette.border,
                      background: notification.read
                        ? theme === "dark"
                          ? "rgba(255,255,255,0.03)"
                          : "rgba(255,255,255,0.8)"
                        : palette.background,
                      borderRadius: 3,
                    }}
                  >
                    <CardContent sx={{ p: 1.8, pb: "16px !important" }}>
                      <Stack spacing={1}>
                        <Stack direction="row" justifyContent="space-between" alignItems="flex-start" spacing={1}>
                          <Box sx={{ minWidth: 0 }}>
                            <Typography sx={{ fontWeight: 800, lineHeight: 1.2 }}>{notification.title}</Typography>
                            <Typography sx={{ fontSize: "0.9rem", mt: 0.55, color: theme === "dark" ? "rgba(248,246,240,0.8)" : "rgba(0,0,0,0.74)" }}>
                              {notification.message}
                            </Typography>
                          </Box>
                          <Chip size="small" label={notification.type} sx={{ textTransform: "capitalize" }} />
                        </Stack>

                        <Stack direction="row" justifyContent="space-between" alignItems="center" spacing={1}>
                          <Typography sx={{ fontSize: "0.76rem", color: theme === "dark" ? "rgba(248,246,240,0.55)" : "rgba(0,0,0,0.55)" }}>
                            {notification.source || "system"}
                          </Typography>

                          <Stack direction="row" spacing={1}>
                            {notification.action_label && notification.action_path && (
                              <Button
                                size="small"
                                variant="contained"
                                endIcon={<OpenInNewRoundedIcon fontSize="small" />}
                                onClick={() => void handleOpenPath(notification.id, notification.action_path)}
                                sx={{
                                  textTransform: "none",
                                  backgroundColor: accentColor,
                                  color: theme === "dark" ? "#111" : "#fff",
                                }}
                              >
                                {notification.action_label}
                              </Button>
                            )}

                            {!notification.read && (
                              <Button size="small" variant="text" onClick={() => void markAsRead(notification.id)}>
                                Mark read
                              </Button>
                            )}
                          </Stack>
                        </Stack>
                      </Stack>
                    </CardContent>
                  </Card>
                );
              })
            )}
          </Stack>
        </Box>
      </Drawer>
    </>
  );
};

const PaperLike = ({ children }: { children: React.ReactNode }) => (
  <Box
    sx={{
      p: 2,
      borderRadius: 3,
      background: "rgba(127,127,127,0.08)",
      border: "1px dashed rgba(127,127,127,0.22)",
    }}
  >
    {children}
  </Box>
);

export default NotificationCenter;