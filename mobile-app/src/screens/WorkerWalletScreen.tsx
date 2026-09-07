import { useEffect, useState } from "react";
import { Pressable, SafeAreaView, StyleSheet, Text, TextInput, View } from "react-native";

import api from "@/services/api";
import { colors } from "@/theme/colors";
import { BankAccountOut, CashoutResponse, PayoutResponse, WalletResponse } from "@/types/api";

export function WorkerWalletScreen() {
  const [wallet, setWallet] = useState<WalletResponse | null>(null);
  const [accounts, setAccounts] = useState<BankAccountOut[]>([]);
  const [bankName, setBankName] = useState("");
  const [accountHolder, setAccountHolder] = useState("");
  const [accountLast4, setAccountLast4] = useState("");
  const [selectedAccount, setSelectedAccount] = useState<string>("");
  const [payoutAmount, setPayoutAmount] = useState("");
  const [cashoutAmount, setCashoutAmount] = useState("");
  const [statusMsg, setStatusMsg] = useState<string | null>(null);

  useEffect(() => {
    api
      .get<WalletResponse>("/payments/worker/wallet")
      .then((res) => setWallet(res.data))
      .catch(() => setWallet(null));

    api
      .get<BankAccountOut[]>("/payments/worker/bank-accounts")
      .then((res) => {
        setAccounts(res.data);
        if (res.data[0]) {
          setSelectedAccount(res.data[0].id);
        }
      })
      .catch(() => setAccounts([]));
  }, []);

  const refreshWallet = () => {
    api
      .get<WalletResponse>("/payments/worker/wallet")
      .then((res) => setWallet(res.data))
      .catch(() => setWallet(null));
  };

  const addBankAccount = async () => {
    setStatusMsg(null);
    if (!bankName || !accountHolder || accountLast4.length !== 4) {
      setStatusMsg("Fill in bank name, account holder, and last 4 digits.");
      return;
    }
    try {
      const { data } = await api.post<BankAccountOut>("/payments/worker/bank-accounts", {
        bank_name: bankName,
        account_holder: accountHolder,
        account_number_last4: accountLast4,
      });
      setAccounts((prev) => [data, ...prev]);
      setSelectedAccount(data.id);
      setBankName("");
      setAccountHolder("");
      setAccountLast4("");
      setStatusMsg("Bank account added.");
    } catch (err) {
      setStatusMsg("Failed to add bank account.");
    }
  };

  const payoutToBank = async () => {
    setStatusMsg(null);
    const amount = Number(payoutAmount);
    if (!selectedAccount) {
      setStatusMsg("Select a bank account.");
      return;
    }
    if (!amount || amount <= 0) {
      setStatusMsg("Enter a valid payout amount.");
      return;
    }
    try {
      const { data } = await api.post<PayoutResponse>("/payments/worker/payout", {
        bank_account_id: selectedAccount,
        amount_cents: Math.round(amount * 100),
      });
      setWallet((prev) => (prev ? { ...prev, balance_cents: data.wallet_balance_cents } : prev));
      setPayoutAmount("");
      setStatusMsg(`Payout ${data.status}.`);
    } catch (err) {
      setStatusMsg("Payout failed.");
    }
  };

  const cashoutAtm = async () => {
    setStatusMsg(null);
    const amount = Number(cashoutAmount);
    if (!amount || amount <= 0) {
      setStatusMsg("Enter a valid cash-out amount.");
      return;
    }
    try {
      const { data } = await api.post<CashoutResponse>("/payments/worker/cashout", {
        amount_cents: Math.round(amount * 100),
      });
      setWallet((prev) => (prev ? { ...prev, balance_cents: data.wallet_balance_cents } : prev));
      setCashoutAmount("");
      setStatusMsg(`Voucher issued: ${data.voucher_code_masked}.`);
    } catch (err) {
      setStatusMsg("Cash-out failed.");
    }
  };

  return (
    <SafeAreaView style={styles.page}>
      <View style={styles.container}>
        <Text style={styles.title}>Worker Wallet</Text>
        <Text style={styles.kpiValue}>
          {wallet ? `R ${(wallet.balance_cents / 100).toFixed(2)}` : "R 0.00"}
        </Text>
        <Pressable style={styles.secondaryAction} onPress={refreshWallet}>
          <Text style={styles.secondaryText}>Refresh</Text>
        </Pressable>

        <View style={styles.card}>
          <Text style={styles.sectionTitle}>Add Bank Account</Text>
          <TextInput style={styles.input} value={bankName} onChangeText={setBankName} placeholder="Bank name" />
          <TextInput
            style={styles.input}
            value={accountHolder}
            onChangeText={setAccountHolder}
            placeholder="Account holder"
          />
          <TextInput
            style={styles.input}
            value={accountLast4}
            onChangeText={setAccountLast4}
            placeholder="Account last 4 digits"
            keyboardType="numeric"
          />
          <Pressable style={styles.action} onPress={addBankAccount}>
            <Text style={styles.actionText}>Add Bank</Text>
          </Pressable>
        </View>

        <View style={styles.card}>
          <Text style={styles.sectionTitle}>Withdraw to Bank</Text>
          <TextInput
            style={styles.input}
            value={selectedAccount}
            onChangeText={setSelectedAccount}
            placeholder="Bank account ID"
          />
          <TextInput
            style={styles.input}
            value={payoutAmount}
            onChangeText={setPayoutAmount}
            placeholder="Amount (ZAR)"
            keyboardType="numeric"
          />
          <Pressable style={styles.action} onPress={payoutToBank}>
            <Text style={styles.actionText}>Send to Bank</Text>
          </Pressable>
        </View>

        <View style={styles.card}>
          <Text style={styles.sectionTitle}>ATM Cash-out</Text>
          <TextInput
            style={styles.input}
            value={cashoutAmount}
            onChangeText={setCashoutAmount}
            placeholder="Amount (ZAR)"
            keyboardType="numeric"
          />
          <Pressable style={styles.action} onPress={cashoutAtm}>
            <Text style={styles.actionText}>Generate Voucher</Text>
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
  title: { fontSize: 26, fontWeight: "700", color: colors.text, marginBottom: 10 },
  kpiValue: { fontSize: 28, fontWeight: "700", color: colors.red },
  card: {
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
  action: { marginTop: 12, backgroundColor: colors.red, borderRadius: 16, paddingVertical: 12, alignItems: "center" },
  actionText: { color: "white", fontWeight: "600" },
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

