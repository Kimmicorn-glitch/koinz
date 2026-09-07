import { useState } from "react";
import { Pressable, SafeAreaView, StyleSheet, Text, TextInput, View } from "react-native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";

import api from "@/services/api";
import { saveAuth } from "@/services/auth-storage";
import { colors } from "@/theme/colors";
import { TokenResponse, UserRole } from "@/types/api";

type Props = NativeStackScreenProps<any> & {
  onAuthenticated: (token: string, role: UserRole) => void;
};

export function LoginScreen({ onAuthenticated }: Props) {
  const [email, setEmail] = useState("employer@localhands.com");
  const [password, setPassword] = useState("ChangeMe123!");
  const [error, setError] = useState<string | null>(null);

  const signIn = async () => {
    setError(null);
    try {
      const { data } = await api.post<TokenResponse>("/auth/login", { email, password });
      await saveAuth(data.access_token, data.role);
      onAuthenticated(data.access_token, data.role);
    } catch {
      setError("Login failed. Verify credentials.");
    }
  };

  return (
    <SafeAreaView style={styles.page}>
      <View style={styles.card}>
        <Text style={styles.title}>Local Hands 2.0</Text>
        <Text style={styles.subtitle}>AI-Powered Township Employment Intelligence</Text>
        <TextInput value={email} onChangeText={setEmail} style={styles.input} autoCapitalize="none" placeholder="Email" />
        <TextInput value={password} onChangeText={setPassword} style={styles.input} secureTextEntry placeholder="Password" />
        {error ? <Text style={styles.error}>{error}</Text> : null}
        <Pressable onPress={signIn} style={styles.button}>
          <Text style={styles.buttonText}>Sign In</Text>
        </Pressable>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: "#fff7f8", alignItems: "center", justifyContent: "center", padding: 16 },
  card: {
    width: "100%",
    maxWidth: 420,
    borderRadius: 24,
    backgroundColor: colors.white,
    borderColor: colors.line,
    borderWidth: 1,
    padding: 20,
    shadowColor: colors.red,
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.12,
    shadowRadius: 20,
    elevation: 3,
  },
  title: { fontSize: 24, fontWeight: "700", color: colors.text },
  subtitle: { fontSize: 13, color: colors.muted, marginTop: 4, marginBottom: 16 },
  input: { borderWidth: 1, borderColor: colors.line, borderRadius: 16, paddingHorizontal: 12, paddingVertical: 11, marginBottom: 12 },
  error: { color: colors.red, marginBottom: 8 },
  button: { backgroundColor: colors.red, borderRadius: 16, paddingVertical: 13, alignItems: "center" },
  buttonText: { color: "white", fontWeight: "600" },
});
