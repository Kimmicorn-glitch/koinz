import { useEffect, useState } from "react";
import { Pressable, SafeAreaView, StyleSheet, Text, TextInput, View } from "react-native";

import api from "@/services/api";
import { colors } from "@/theme/colors";
import { FundEmployerResponse, PayWorkerResponse, WalletResponse } from "@/types/api";

export function EmployerDashboardScreen({ navigation }: any) {
  const [wallet, setWallet] = useState<WalletResponse | null>(null);
  const [fundAmount, setFundAmount] = useState("");
  const [workerId, setWorkerId] = useState("");
  const [payAmount, setPayAmount] = useState("");
  const [statusMsg, setStatusMsg] = useState<string | null>(null);

  useEffect(() => {
    api
      .get<WalletResponse>("/payments/employer/wallet")
      .then((res) => setWallet(res.data))
      .catch(() => setWallet(null));
  }, []);

  const refreshWallet = () => {
    api
      .get<WalletResponse>("/payments/employer/wallet")
      .then((res) => setWallet(res.data))
      .catch(() => setWallet(null));
  };

  const handleFund = async () => {
    setStatusMsg(null);
    const amount = Number(fundAmount);
    if (!amount || amount <= 0) {
      setStatusMsg("Enter a valid funding amount.");
      return;
    }
    try {
      const { data } = await api.post<FundEmployerResponse>("/payments/employer/fund", {
        amount_cents: Math.round(amount * 100),
      });
      setWallet((prev) => (prev ? { ...prev, balance_cents: data.wallet_balance_cents } : prev));
      setFundAmount("");
      setStatusMsg(`Funding ${data.status}.`);
    } catch (err) {
      setStatusMsg("Funding failed.");
    }
  };

  const handlePayWorker = async () => {
    setStatusMsg(null);
    const amount = Number(payAmount);
    if (!workerId) {
      setStatusMsg("Enter a worker ID.");
      return;
    }
    if (!amount || amount <= 0) {
      setStatusMsg("Enter a valid payment amount.");
      return;
    }
    try {
      const { data } = await api.post<PayWorkerResponse>("/payments/employer/pay-worker", {
        worker_id: workerId,
        amount_cents: Math.round(amount * 100),
      });
      setWallet((prev) => (prev ? { ...prev, balance_cents: data.employer_balance_cents } : prev));
      setWorkerId("");
      setPayAmount("");
      setStatusMsg("Worker paid.");
    } catch (err) {
      setStatusMsg("Worker payment failed.");
    }
  };

  return (
    <SafeAreaView style={styles.page}>
      <View style={styles.container}>
        <Text style={styles.title}>Employer Dashboard</Text>
        <View style={styles.grid}>
          <View style={styles.card}>
            <Text style={styles.kpiLabel}>Active Jobs</Text>
            <Text style={styles.kpiValue}>247</Text>
          </View>
          <View style={styles.card}>
            <Text style={styles.kpiLabel}>Match Rate</Text>
            <Text style={styles.kpiValue}>82%</Text>
          </View>
        </View>
        <Pressable style={styles.action} onPress={() => navigation.navigate("Jobs")}>
          <Text style={styles.actionText}>Go to Job List</Text>
        </Pressable>

        <View style={styles.cardWide}>
          <Text style={styles.sectionTitle}>Employer Wallet</Text>
          <Text style={styles.kpiValue}>
            {wallet ? `R ${(wallet.balance_cents / 100).toFixed(2)}` : "R 0.00"}
          </Text>
          <Pressable style={styles.secondaryAction} onPress={refreshWallet}>
            <Text style={styles.secondaryText}>Refresh</Text>
          </Pressable>
        </View>

        <View style={styles.cardWide}>
          <Text style={styles.sectionTitle}>Fund Wallet</Text>
          <TextInput
            value={fundAmount}
            onChangeText={setFundAmount}
            style={styles.input}
            keyboardType="numeric"
            placeholder="Amount (ZAR)"
          />
          <Pressable style={styles.action} onPress={handleFund}>
            <Text style={styles.actionText}>Fund</Text>
          </Pressable>
        </View>

        <View style={styles.cardWide}>
          <Text style={styles.sectionTitle}>Pay Worker</Text>
          <TextInput value={workerId} onChangeText={setWorkerId} style={styles.input} placeholder="Worker ID" />
          <TextInput
            value={payAmount}
            onChangeText={setPayAmount}
            style={styles.input}
            keyboardType="numeric"
            placeholder="Amount (ZAR)"
          />
          <Pressable style={styles.action} onPress={handlePayWorker}>
            <Text style={styles.actionText}>Pay</Text>
          </Pressable>
        </View>

        {statusMsg ? <Text style={styles.status}>{statusMsg}</Text> : null}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: "#fff7f8" },
  container: { padding: 16 },
  title: { fontSize: 26, fontWeight: "700", color: colors.text, marginBottom: 16 },
  grid: { flexDirection: "row", gap: 10 },
  card: { flex: 1, borderRadius: 20, borderWidth: 1, borderColor: colors.line, backgroundColor: colors.white, padding: 14 },
  kpiLabel: { color: colors.muted },
  kpiValue: { marginTop: 8, fontSize: 24, fontWeight: "700", color: colors.red },
  action: { marginTop: 18, backgroundColor: colors.red, borderRadius: 16, paddingVertical: 12, alignItems: "center" },
  actionText: { color: "white", fontWeight: "600" },
  cardWide: {
    marginTop: 16,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: colors.line,
    backgroundColor: colors.white,
    padding: 16,
  },
  sectionTitle: { fontSize: 16, fontWeight: "600", color: colors.text },
  input: {
    marginTop: 10,
    borderRadius: 14,
    borderWidth: 1,
    borderColor: colors.line,
    paddingHorizontal: 12,
    paddingVertical: 10,
    backgroundColor: "#fff",
  },
  secondaryAction: {
    marginTop: 10,
    borderRadius: 16,
    paddingVertical: 10,
    alignItems: "center",
    borderWidth: 1,
    borderColor: colors.line,
  },
  secondaryText: { color: colors.text, fontWeight: "600" },
  status: { marginTop: 12, color: colors.muted },
});
