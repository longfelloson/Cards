import { useEffect, useState } from "react";
import { updateUserEmail } from "../users";
import Layout from "../components/Layout";
import { useSearchParams } from "react-router-dom";
import VerificationPending from "../components/verification/VerificationPending";
import VerificationSuccess from "../components/verification/VerificationSuccess";
import VerificationFailure from "../components/verification/VerificationFailure";

const VerificationPage = () => {
  const [searchParams] = useSearchParams();
  const [verificationStatus, setVerificationStatus] = useState('pending');
  const userId = searchParams.get("user_id");
  const token = searchParams.get("token");
  const newEmail = searchParams.get("email");

  useEffect(() => {
  const newEmail = searchParams.get("email");
    const response = updateUserEmail(newEmail, token, userId)
    if (response.status_code !== 400) {
      setVerificationStatus("success");
    } else {
      setVerificationStatus("failure")
    }
  }, [])

  return (
    <Layout>
      { 
        verificationStatus === "pending" 
        ? <VerificationPending /> 
        : verificationStatus === "success" ? <VerificationSuccess /> : <VerificationFailure />  
      }
    </Layout>
  )
};

export default VerificationPage