import { StyleSheet, Text, View } from "react-native";

import { colors } from "@/theme/colors";

export function WorkerProfileCard() {
  return (
    <View style={styles.card}>
      <View style={styles.square} />
      <Text style={styles.name}>Nomsa Dlamini</Text>
      <Text style={styles.meta}>Khayelitsha • Electrical • Safety</Text>
      <Text style={styles.match}>Match Readiness: 89%</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.white,
    borderColor: colors.line,
    borderWidth: 1,
    borderRadius: 22,
    padding: 16,
    shadowColor: colors.red,
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.08,
    shadowRadius: 16,
    elevation: 2,
  },
  square: {
    width: 26,
    height: 26,
    borderRadius: 8,
    backgroundColor: colors.red,
    marginBottom: 10,
  },
  name: { fontSize: 18, fontWeight: "700", color: colors.text },
  meta: { marginTop: 6, color: colors.muted },
  match: { marginTop: 10, color: colors.red, fontWeight: "600" },
});
