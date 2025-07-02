import React, { useState, useEffect } from "react";
import { useAuth } from "./AuthContext";
import { useNavigate } from "react-router-dom";

function ListUser() {
  const { token, loading: authLoading } = useAuth();
  const navigate = useNavigate(); // ← Ajout essentiel ici 👈
  const [users, setUsers] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [search, setSearch] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedUser, setSelectedUser] = useState(null);

  useEffect(() => {
    if (authLoading) return;

    if (!token) {
      setError("Aucun token trouvé. Veuillez vous connecter.");
      setLoading(false);
      return;
    }

    const fetchUsers = async () => {
      try {
        const res = await fetch("http://localhost:8000/auth/all/", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!res.ok) throw new Error(`Erreur API (${res.status})`);
        const data = await res.json();

        setUsers(data);
        setFiltered(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, [token, authLoading]);

  const handleSearch = (e) => {
    const value = e.target.value.toLowerCase();
    setSearch(value);
    const results = users.filter(
      (u) =>
        u.first_name?.toLowerCase().includes(value) ||
        u.last_name?.toLowerCase().includes(value) ||
        u.username?.toLowerCase().includes(value) ||
        u.name?.toLowerCase().includes(value)
    );
    setFiltered(results);
  };

  const getFullName = (user) => {
    const fullName = `${user.first_name || ""} ${user.last_name || ""}`.trim();
    return fullName || user.name || "Nom inconnu";
  };

  if (loading) return <p className="text-center mt-5">Chargement...</p>;
  if (error) return <p className="text-danger text-center mt-5">{error}</p>;

  return (
    <div className="container py-5">
      <h2 className="text-center mb-4">Liste des utilisateurs</h2>

      <div className="mb-4 d-flex justify-content-center">
        <input
          type="text"
          value={search}
          onChange={handleSearch}
          placeholder="Rechercher"
          className="form-control text-center shadow-sm"
          style={{ maxWidth: "400px", background: "#f1f1f1", borderRadius: "30px" }}
        />
      </div>

      <div className="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4">
        {filtered.map((user) => (
          <div key={user.id} className="col">
            <div className="card h-100 text-center border-0 shadow-sm">
              <div className="card-body d-flex flex-column justify-content-center">
                <div className="mb-2">
                  <p>{getFullName(user)}</p>
                </div>
                <button
                  className="btn btn-outline-dark btn-sm mb-2"
                  onClick={() => setSelectedUser(user)}
                >
                  Détails
                </button>
                <button
                  className="btn btn-outline-dark btn-sm"
                  onClick={() => navigate(`/stats/${user.id}`)}
                >
                  Statistiques
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {selectedUser && (
        <div className="modal d-block" tabIndex="-1" style={{ background: "rgba(0,0,0,0.5)" }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">
                  Détail : {getFullName(selectedUser)}
                </h5>
                <button
                  type="button"
                  className="btn-close"
                  onClick={() => setSelectedUser(null)}
                />
              </div>
              <div className="modal-body">
                <p><strong>Email :</strong> {selectedUser.email}</p>
                <p><strong>Username :</strong> {selectedUser.username}</p>
                <p><strong>Prénom :</strong> {selectedUser.first_name}</p>
              </div>
              <div className="modal-footer">
                <button className="btn btn-secondary" onClick={() => setSelectedUser(null)}>
                  Fermer
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ListUser;
