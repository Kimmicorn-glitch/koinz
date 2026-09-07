import { useEffect, useState } from "react";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

import { EmployerDashboardScreen } from "@/screens/EmployerDashboardScreen";
import { JobsScreen } from "@/screens/JobsScreen";
import { LoginScreen } from "@/screens/LoginScreen";
import { MatchScreen } from "@/screens/MatchScreen";
import { ProfileScreen } from "@/screens/ProfileScreen";
import { WorkerWalletScreen } from "@/screens/WorkerWalletScreen";
import { getRole, getToken } from "@/services/auth-storage";
import { UserRole } from "@/types/api";

type RootStackParams = {
  Login: undefined;
  EmployerDashboard: undefined;
  WorkerWallet: undefined;
  Profile: undefined;
  Jobs: undefined;
  Match: undefined;
};

const Stack = createNativeStackNavigator<RootStackParams>();

export function RootNavigator() {
  const [ready, setReady] = useState(false);
  const [token, setToken] = useState<string | null>(null);
  const [role, setRole] = useState<UserRole | null>(null);

  useEffect(() => {
    Promise.all([getToken(), getRole()]).then(([storedToken, storedRole]) => {
      setToken(storedToken);
      setRole(storedRole);
      setReady(true);
    });
  }, []);

  if (!ready) {
    return null;
  }

  return (
    <Stack.Navigator screenOptions={{ headerShadowVisible: false }}>
      {!token ? (
        <Stack.Screen name="Login" options={{ headerShown: false }}>
          {(props) => (
            <LoginScreen
              {...props}
              onAuthenticated={(nextToken, nextRole) => {
                setToken(nextToken);
                setRole(nextRole);
              }}
            />
          )}
        </Stack.Screen>
      ) : role === "employer" || role === "admin" ? (
        <>
          <Stack.Screen name="EmployerDashboard" component={EmployerDashboardScreen} options={{ title: "Employer" }} />
          <Stack.Screen name="Jobs" component={JobsScreen} />
          <Stack.Screen name="Match" component={MatchScreen} />
        </>
      ) : (
        <>
          <Stack.Screen name="WorkerWallet" component={WorkerWalletScreen} options={{ title: "Wallet" }} />
          <Stack.Screen name="Profile" component={ProfileScreen} options={{ title: "Worker" }} />
          <Stack.Screen name="Jobs" component={JobsScreen} />
          <Stack.Screen name="Match" component={MatchScreen} />
        </>
      )}
    </Stack.Navigator>
  );
}
