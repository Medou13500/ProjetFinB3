
import {
  updateEmail,
  EmailAuthProvider,
  reauthenticateWithCredential,
} from "firebase/auth";

export const updateUserEmail = async (auth, currentPassword, newEmail) => {
  const user = auth.currentUser;

  if (!user) {
    throw new Error("Aucun utilisateur connecté.");
  }

  const credential = EmailAuthProvider.credential(user.email, currentPassword);

  try {
    // Re-authentifie l'utilisateur
    await reauthenticateWithCredential(user, credential);

    // Met à jour l'e-mail
    await updateEmail(user, newEmail);

    return { success: true, message: "Email mis à jour avec succès." };
  } catch (error) {
    console.error("Erreur lors de la mise à jour de l'e-mail :", error);
    return { success: false, message: error.message };
  }
};
