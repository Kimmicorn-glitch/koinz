import { FlatList, Pressable, SafeAreaView, StyleSheet, Text, View } from "react-native";

import { colors } from "@/theme/colors";

const jobs = [
  { id: "job-001", title: "Electrical Assistant", location: "Khayelitsha" },
  { id: "job-002", title: "Plumbing Support", location: "Soweto" },
];

export function JobsScreen({ navigation }: any) {
  return (
    <SafeAreaView style={styles.page}>
      <FlatList
        contentContainerStyle={styles.content}
        data={jobs}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <Pressable style={styles.card} onPress={() => navigation.navigate("Match", { jobId: item.id })}>
            <Text style={styles.title}>{item.title}</Text>
            <Text style={styles.location}>{item.location}</Text>
          </Pressable>
        )}
        ListHeaderComponent={<Text style={styles.heading}>Job List</Text>}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: "#fff7f8" },
  content: { padding: 16, gap: 10 },
  heading: { fontSize: 24, fontWeight: "700", color: colors.text, marginBottom: 6 },
  card: { backgroundColor: colors.white, borderRadius: 18, borderWidth: 1, borderColor: colors.line, padding: 14 },
  title: { fontSize: 17, fontWeight: "600", color: colors.text },
  location: { marginTop: 4, color: colors.muted },
});
