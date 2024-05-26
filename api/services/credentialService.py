import subprocess
from fastapi import HTTPException

def refresh_credentials(profile_name):
    try:
        # Atualizar as credenciais do AWS SSO para o perfil especificado
        result = subprocess.run(["aws", "sso", "login", "--profile", profile_name], check=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(result.stderr)
        return {"message": "Credenciais atualizadas com sucesso."}
    except subprocess.CalledProcessError as e:
        # Exibir mensagem de erro caso ocorra uma exceção ao atualizar as credenciais
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar as credenciais: {e}")