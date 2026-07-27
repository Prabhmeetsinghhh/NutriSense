import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";
import axios from "../api/axiosInstance";

export type NotificationType = "info" | "success" | "warning" | "error";

export type NotificationItem = {
  id: string;
  title: string;
  message: string;
  type: NotificationType;
  priority?: string;
  source?: string;
  action_label?: string | null;
  action_path?: string | null;
  read: boolean;
  created_at?: string;
  read_at?: string | null;
};

type NotificationContextValue = {
  notifications: NotificationItem[];
  unreadCount: number;
  loading: boolean;
  refreshNotifications: () => Promise<void>;
  markAsRead: (notificationId: string) => Promise<void>;
  markAllAsRead: () => Promise<void>;
};

const NotificationContext = createContext<NotificationContextValue | undefined>(undefined);

const getStoredEmail = () => localStorage.getItem("nutrisenseUser")?.trim().toLowerCase() || "";

export const NotificationProvider = ({ children }: { children: ReactNode }) => {
  const [email, setEmail] = useState(getStoredEmail);
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchNotifications = useCallback(async () => {
    const currentEmail = getStoredEmail();
    setEmail(currentEmail);

    if (!currentEmail) {
      setNotifications([]);
      return;
    }

    setLoading(true);
    try {
      const response = await axios.get(`/notifications/${currentEmail}?limit=12`);
      if (response.data.status === "success") {
        setNotifications(response.data.notifications ?? []);
      }
    } catch (error) {
      console.error("Failed to fetch notifications:", error);
      setNotifications([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void fetchNotifications();

    const syncEmail = () => {
      const nextEmail = getStoredEmail();
      setEmail(nextEmail);
      void fetchNotifications();
    };

    window.addEventListener("focus", syncEmail);
    window.addEventListener("storage", syncEmail);
    window.addEventListener("nutrisense-auth-changed", syncEmail as EventListener);

    return () => {
      window.removeEventListener("focus", syncEmail);
      window.removeEventListener("storage", syncEmail);
      window.removeEventListener("nutrisense-auth-changed", syncEmail as EventListener);
    };
  }, []);

  const refreshNotifications = useCallback(async () => {
    await fetchNotifications();
  }, [fetchNotifications]);

  const markAsRead = useCallback(async (notificationId: string) => {
    if (!email) return;

    try {
      await axios.post(`/notifications/${email}/${notificationId}/read`);
      await fetchNotifications();
    } catch (error) {
      console.error("Failed to mark notification as read:", error);
    }
  }, [email, fetchNotifications]);

  const markAllAsRead = useCallback(async () => {
    if (!email) return;

    try {
      await axios.post(`/notifications/${email}/read-all`);
      await fetchNotifications();
    } catch (error) {
      console.error("Failed to mark notifications as read:", error);
    }
  }, [email, fetchNotifications]);

  const unreadCount = useMemo(
    () => notifications.filter((notification) => !notification.read).length,
    [notifications]
  );

  const contextValue = useMemo(
    () => ({
      notifications,
      unreadCount,
      loading,
      refreshNotifications,
      markAsRead,
      markAllAsRead,
    }),
    [loading, markAllAsRead, markAsRead, notifications, refreshNotifications, unreadCount]
  );

  return <NotificationContext.Provider value={contextValue}>{children}</NotificationContext.Provider>;
};

export const useNotifications = () => {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error("useNotifications must be used within NotificationProvider");
  }

  return context;
};