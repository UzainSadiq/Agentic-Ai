from pathlib import Path
def test_files():
    root=Path(__file__).resolve().parents[1]
    for name in ['app.py','agent.py','rag.py','config.py','build_index.py','.env.example','requirements.txt']:
        assert (root/name).exists()
