function Login({ onSignIn }) {
  const [email, setEmail] = React.useState("anika@northfield.co");
  return (
    <div style={{ height: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: "#FCFCFD", fontFamily: "Inter" }}>
      <div style={{ width: 400, padding: 32, background: "white", borderRadius: 16, boxShadow: "0 25px 50px -12px rgba(0,0,0,0.12)", border: "1px solid #EDEFF3" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 28 }}>
          <img src="../../assets/favicon.svg" width="36" height="36" />
          <div style={{ font: "700 22px/1 Inter", letterSpacing: "-0.4px", color: "#12172B" }}>OneCap</div>
        </div>
        <div style={{ font: "700 20px/28px Inter", letterSpacing: "-0.2px", marginBottom: 6 }}>Sign in to your workspace</div>
        <div style={{ font: "400 13px/20px Inter", color: "#6C727F", marginBottom: 22 }}>Use your work email. We'll send a single-use sign-in link.</div>
        <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
          <Input label="Email Address" leftIcon="mail" value={email} onChange={setEmail} placeholder="name@company.com" />
          <Button variant="primary" size="lg" onClick={onSignIn} style={{ width: "100%", justifyContent: "center" }}>Continue</Button>
        </div>
        <div style={{ marginTop: 18, textAlign: "center", font: "400 12px/16px Inter", color: "#6C727F" }}>
          Trouble signing in? <a style={{ color: "#01187D", fontWeight: 500, textDecoration: "none" }}>Contact support</a>
        </div>
      </div>
    </div>
  );
}

Object.assign(window, { Login });
