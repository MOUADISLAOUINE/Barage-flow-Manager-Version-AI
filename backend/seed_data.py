"""
seed_data.py — Populate the database with realistic development data for French models.
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from datetime import datetime, timedelta, date
from app.database import SessionLocal, engine, Base
from app.models import (
    Barrage, Utilisateur, Cooperative, OrdreLiberation,
    Capteur, LectureCapteur, Contrat, ResultatPrevision, JournalAudit
)
# from app.core.security import hash_password

def hash_password(p):
    # Dummy/Hardcoded hash for development to bypass bcrypt environment issues
    return "$2b$12$LQv3c1yqBWVHxkd0LpPbbeeK99T5Y4C8.SY8nOq91K./I6YpU.Ouy" 

Base.metadata.create_all(bind=engine)
db = SessionLocal()

def seed():
    print("🌱 Seeding development database with French models...")
    
    # ── Barrage ───────────────────────────────────────────────────────
    barrage = Barrage(
        nom="Youssef Ibn Tachfine Dam",
        localisation_gps="29.8833,-9.7167",
        capacite_max_m3=296_000_000,
        seuil_reserve_m3=74_000_000,
        niveau_actuel_m3=165_760_000,
        derniere_maj=datetime.utcnow()
    )
    db.add(barrage)
    db.flush()

    # ── Utilisateurs ─────────────────────────────────────────────────────────
    utilisateurs = [
        Utilisateur(nom="Hassan El Mansouri", email="director@barrage.ma",
                    mot_de_passe_hash=hash_password("director123!"),
                    role="Directeur", statut="actif", mfa_active=False),
        Utilisateur(nom="Fatima Zahra Benali", email="operator1@barrage.ma",
                    mot_de_passe_hash=hash_password("operator123!"),
                    role="Operateur", statut="actif", mfa_active=False),
        Utilisateur(nom="Nadia Tazi", email="officer@barrage.ma",
                    mot_de_passe_hash=hash_password("officer123!"),
                    role="Officier", statut="actif", mfa_active=False),
        Utilisateur(nom="Karim Lahlou", email="admin@barrage.ma",
                    mot_de_passe_hash=hash_password("admin123!"),
                    role="Admin", statut="actif", mfa_active=False),
    ]
    for u in utilisateurs:
        db.add(u)
    db.flush()

    # ── Capteurs ───────────────────────────────────────────────────────
    capteurs = [
        Capteur(id_barrage=barrage.id_barrage, type_capteur="niveau",
                localisation="Main Level Gauge", unite_mesure="m³",
                statut="OK", derniere_calibration=date(2025, 1, 15)),
        Capteur(id_barrage=barrage.id_barrage, type_capteur="debit",
                localisation="Outlet Flow Meter", unite_mesure="m³/s",
                statut="OK", derniere_calibration=date(2025, 2, 10)),
        Capteur(id_barrage=barrage.id_barrage, type_capteur="pluie",
                localisation="Rain Gauge Station 1", unite_mesure="mm",
                statut="PANNE", derniere_calibration=date(2024, 11, 5)),
        Capteur(id_barrage=barrage.id_barrage, type_capteur="vanne",
                localisation="Main Gate", unite_mesure="open/closed",
                statut="OK", derniere_calibration=date(2025, 3, 1)),
    ]
    for c in capteurs:
        db.add(c)
    db.flush()

    # ── LectureCapteur ────────────────────────────────────────────────
    now = datetime.utcnow()
    lectures = [
        LectureCapteur(id_capteur=capteurs[0].id_capteur, timestamp=now - timedelta(minutes=10), valeur=165760000.0, indicateur_qualite="reel"),
        LectureCapteur(id_capteur=capteurs[1].id_capteur, timestamp=now - timedelta(minutes=10), valeur=12.5, indicateur_qualite="reel"),
        LectureCapteur(id_capteur=capteurs[2].id_capteur, timestamp=now - timedelta(minutes=10), valeur=0.0, indicateur_qualite="defectueux"),
        LectureCapteur(id_capteur=capteurs[3].id_capteur, timestamp=now - timedelta(minutes=10), valeur=1.0, indicateur_qualite="reel"),
    ]
    for lc in lectures:
        db.add(lc)

    # ── Cooperatives ─────────────────────────────────────────────────
    coops = [
        Cooperative(nom="Coopérative Ajdal", region="Tiznit Nord",
                    superficie_ha=850.5, types_cultures="Argan, Orge",
                    classe_priorite="A", nom_contact="Mohamed Abargh", email_contact="ajdal@coops.ma"),
        Cooperative(nom="Coopérative Tafraout", region="Tafraout",
                    superficie_ha=620.0, types_cultures="Blé, Maïs",
                    classe_priorite="B", nom_contact="Aicha Idbassaid", email_contact="tafraout@coops.ma"),
        Cooperative(nom="Coopérative Souss Vert", region="Tiznit Sud",
                    superficie_ha=430.2, types_cultures="Légumes",
                    classe_priorite="C", nom_contact="Omar Chafai", email_contact="soussvert@coops.ma"),
    ]
    for c in coops:
        db.add(c)
    db.flush()

    # ── Contrats ──────────────────────────────────────────────────────
    season_start = date(2025, 6, 1)
    season_end = date(2025, 10, 31)
    contrats = [
        Contrat(id_cooperative=coops[0].id_cooperative, id_barrage=barrage.id_barrage,
                saison="Ete 2025", volume_contracte_m3=620_000, poids_priorite=1.5,
                statut="actif", date_debut=season_start, date_fin=season_end),
        Contrat(id_cooperative=coops[1].id_cooperative, id_barrage=barrage.id_barrage,
                saison="Ete 2025", volume_contracte_m3=450_000, poids_priorite=1.0,
                statut="actif", date_debut=season_start, date_fin=season_end),
        Contrat(id_cooperative=coops[2].id_cooperative, id_barrage=barrage.id_barrage,
                saison="Ete 2025", volume_contracte_m3=280_000, poids_priorite=0.6,
                statut="actif", date_debut=season_start, date_fin=season_end),
    ]
    for ct in contrats:
        db.add(ct)

    # ── OrdreLiberation ───────────────────────────────────────────────
    ordres = [
        OrdreLiberation(id_demandeur=utilisateurs[1].id_utilisateur, id_approbateur=utilisateurs[0].id_utilisateur,
                        id_cooperative=coops[0].id_cooperative, volume_m3=50000,
                        timestamp_demande=now - timedelta(days=2), timestamp_decision=now - timedelta(days=1),
                        statut="APPROUVE", notes_approbation="Approuvé pour l'irrigation prioritaire."),
        OrdreLiberation(id_demandeur=utilisateurs[1].id_utilisateur, id_approbateur=None,
                        id_cooperative=coops[1].id_cooperative, volume_m3=20000,
                        timestamp_demande=now - timedelta(hours=5), timestamp_decision=None,
                        statut="EN_ATTENTE", notes_approbation=None),
    ]
    for o in ordres:
        db.add(o)
        
    # ── ResultatPrevision ─────────────────────────────────────────────
    prevision = ResultatPrevision(
        id_barrage=barrage.id_barrage,
        date_generation=now,
        version_modele="v1.2.0 LSTM",
        niveaux_predits_json=[165000000, 164500000, 163000000],
        intervalles_confiance_json=[[164000000, 166000000], [163000000, 165000000]],
        score_precision=0.92,
        horizon_jours=3
    )
    db.add(prevision)

    # ── JournalAudit ──────────────────────────────────────────────────
    audits = [
        JournalAudit(id_utilisateur=utilisateurs[0].id_utilisateur, action="LOGIN",
                     entite_concernee="Utilisateur", id_entite=utilisateurs[0].id_utilisateur,
                     donnees_avant_json=None, donnees_apres_json=None, timestamp=now - timedelta(hours=1),
                     adresse_ip="192.168.1.10", id_session="sess_abc123"),
        JournalAudit(id_utilisateur=utilisateurs[0].id_utilisateur, action="APPROVE_ORDER",
                     entite_concernee="OrdreLiberation", id_entite=1,
                     donnees_avant_json={"statut": "EN_ATTENTE"}, donnees_apres_json={"statut": "APPROUVE"},
                     timestamp=now - timedelta(days=1), adresse_ip="192.168.1.10", id_session="sess_def456"),
    ]
    for a in audits:
        db.add(a)

    db.commit()
    print("✅ Seed complete.")

if __name__ == "__main__":
    seed()
    db.close()
