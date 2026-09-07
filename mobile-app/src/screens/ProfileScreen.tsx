import { Pressable, SafeAreaView, ScrollView, StyleSheet, Text } from "react-native";

import { WorkerProfileCard } from "@/components/WorkerProfileCard";
import { colors } from "@/theme/colors";

export function ProfileScreen({ navigation }: any) {
  return (
    <SafeAreaView style={styles.page}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.title}>Worker Profile</Text>
        <WorkerProfileCard />
        <Pressable style={styles.action} onPress={() => navigation.navigate("WorkerWallet")}>
          <Text style={styles.actionText}>Open Wallet</Text>
        </Pressable>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: "#fff7f8" },
  content: { padding: 16, gap: 14 },
  title: { fontSize: 24, fontWeight: "700", color: "#1a1a1a" },
  action: { marginTop: 10, backgroundColor: colors.red, borderRadius: 16, paddingVertical: 12, alignItems: "center" },
  actionText: { color: "white", fontWeight: "600" },
});
