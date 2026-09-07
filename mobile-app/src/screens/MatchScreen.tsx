import { useEffect, useState } from "react";
import { SafeAreaView, StyleSheet, Text, View } from "react-native";

import api from "@/services/api";
import { colors } from "@/theme/colors";
import { MatchResponse } from "@/types/api";

export function MatchScreen({ route }: any) {
  const jobId = route?.params?.jobId ?? "job-001";
  const [data, setData] = useState<MatchResponse | null>(null);

  useEffect(() => {
    api
      .get<MatchResponse>(`/matches/${jobId}`)
      .then((res) => setData(res.data))
      .catch(() => setData(null));
  }, [jobId]);

  return (
    <SafeAreaView style={styles.page}>
      <View style={styles.container}>
        <Text style={styles.title}>Match Screen</Text>
        <Text style={styles.subtitle}>Job: {jobId}</Text>
        {(data?.matches ?? []).map((match) => (
          <View style={styles.card} key={match.profile_id}>
            <Text style={styles.name}>{match.profile_id}</Text>
            <Text style={styles.score}>Score: {Math.round(match.score * 100)}%</Text>
          </View>
        ))}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: "#fff7f8" },
  container: { padding: 16 },
  title: { fontSize: 24, fontWeight: "700", color: colors.text },
  subtitle: { color: colors.muted, marginBottom: 14 },
  card: { backgroundColor: colors.white, borderWidth: 1, borderColor: colors.line, borderRadius: 18, padding: 12, marginBottom: 10 },
  name: { fontWeight: "600", color: colors.text },
  score: { color: colors.red, marginTop: 4 },
});
