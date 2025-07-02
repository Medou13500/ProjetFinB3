import React, { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
} from "recharts";
import { useAuth } from "./AuthContext";

function UserStats() {
  const { token } = useAuth();
  const [data, setData] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchStats = async () => {
      try {
      const res = await fetch("http://localhost:8000/runs/stats/monthly/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        
        });
        
        if (!res.ok) {
          const errText = await res.text();
          throw new Error(errText || "Erreur lors de la récupération.");
        }

        const jsonData = await res.json();

        let formattedData = [];
        if (jsonData && typeof jsonData === "object" && !Array.isArray(jsonData)) {
          formattedData = [jsonData];
        } else if (Array.isArray(jsonData)) {
          formattedData = jsonData;
        } else {
          throw new Error("Format de données inattendu.");
        }

        // 🔒 Sécurité : on force les valeurs numériques
        formattedData = formattedData.map((entry) => ({
          ...entry,
          total_distance_km: parseFloat(entry.total_distance_km) || 0,
          estimated_calories: parseFloat(entry.estimated_calories) || 0,
        }));

        setData(formattedData);
      } catch (err) {
        setError(err.message || "Une erreur est survenue.");
      }
    };

    if (token) {
      fetchStats();
    }
  }, [token]);

  if (error) {
    return <p className="text-danger text-center mt-5">{error}</p>;
  }

  if (!data.length) {
    return <p className="text-center mt-5">Chargement des statistiques mensuelles...</p>;
  }

  return (
    <div className="container mt-5">
      <h3 className="text-center mb-4">Statistiques mensuelles de course</h3>
      <pre>{JSON.stringify(data, null, 2)}</pre>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={data} margin={{ top: 20, right: 30, bottom: 5, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" />
         <XAxis dataKey="month" />
          <YAxis domain={[0, "dataMax + 100"]} />
          <Tooltip
            formatter={(value, name) => {
              const labels = {
                total_distance_km: "Distance totale (km)",
                estimated_calories: "Calories estimées",
              };
              return [value, labels[name] || name];
            }}
          />
          <Legend />
          <Bar
            dataKey="total_distance_km"
            fill="#8884d8"
            name="Distance totale (km)"
            barSize={50}
            minPointSize={5}
          />
          <Bar
            dataKey="estimated_calories"
            fill="#82ca9d"
            name="Calories estimées"
            barSize={50}
            minPointSize={5}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default UserStats;
