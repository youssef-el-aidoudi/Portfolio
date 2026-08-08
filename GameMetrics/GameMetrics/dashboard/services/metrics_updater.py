import os
import sys
import subprocess
from pathlib import Path


def run_metrics_update() -> tuple[bool, str]:
    """
    Lance `python/update_game_metrics.py` en subprocess et capture sa sortie.

    Returns:
        (success: bool, output: str) — True si returncode == 0.
    """
    # Remonte depuis dashboard/services/ jusqu'à la racine du projet
    project_root = Path(__file__).resolve().parent.parent.parent
    script_path = project_root / "python" / "update_game_metrics.py"

    if not script_path.exists():
        return False, f"Script introuvable : {script_path}"

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=str(project_root),
            timeout=30,  # évite un blocage indéfini
        )

        if result.returncode == 0:
            return True, result.stdout or "Mise à jour terminée sans sortie."
        else:
            error_msg = result.stderr or result.stdout or "Erreur inconnue."
            return False, error_msg

    except subprocess.TimeoutExpired:
        return False, "Timeout : le script a mis plus de 30 secondes à s'exécuter."
    except FileNotFoundError:
        return False, f"Python introuvable : {sys.executable}"
    except Exception as e:
        return False, f"Erreur subprocess : {e}"
