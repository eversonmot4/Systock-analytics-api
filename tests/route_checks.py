#!/usr/bin/env python3
import os
import sys
import pathlib
import importlib
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("DB_VIEW_PREFIX", "")

# Garante que a raiz do projeto esteja em sys.path e carrega main.py como um módulo pelo caminho
ROOT = pathlib.Path(__file__).parents[1].resolve()
sys.path.insert(0, str(ROOT))
import importlib.util
spec = importlib.util.spec_from_file_location("main", str(ROOT / "main.py"))
main = importlib.util.module_from_spec(spec)
sys.modules["main"] = main
spec.loader.exec_module(main)
app = main.app

# importa módulos dos routers via importlib para que possamos substituir o fetch_view em nível de módulo
vendas = importlib.import_module("routers.vendas")
lojas = importlib.import_module("routers.lojas")
categorias = importlib.import_module("routers.categorias")
produtos = importlib.import_module("routers.produtos")
estoque = importlib.import_module("routers.estoque")
repository = importlib.import_module("services.repository")


def mock_fetch(view_name: str):
    # retorna uma linha mock previsível para cada view
    return [{"view": view_name, "sample_value": 1}]


# Substitui referências no nível do módulo para fetch_view, fazendo com que os routers chamem o mock
for mod in (vendas, lojas, categorias, produtos, estoque):
    setattr(mod, "fetch_view", mock_fetch)

# Também substitui `repository.fetch_view`
repository.fetch_view = mock_fetch


from fastapi.testclient import TestClient


def main():
    client = TestClient(app)

    endpoints = [
        "/vendas/evolucao",
        "/vendas/semanais",
        "/lojas/performance",
        "/categorias/top",
        "/produtos/top",
        "/estoque/valor-atual",
    ]

    failures = []
    for path in endpoints:
        r = client.get(path)
        ok = r.status_code == 200
        print(path, "->", r.status_code)
        if not ok:
            failures.append((path, r.status_code, r.text))

    if failures:
        print("Failures:\n", failures)
        raise SystemExit(1)
    print("All routes responded with 200 OK (mocked repository).")


if __name__ == "__main__":
    main()