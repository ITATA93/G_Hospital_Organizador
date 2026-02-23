import os

from src.architect.planner import StructureArchitect
from src.audit.vault import AuditVault

print("Initializing Vault...")
vault = AuditVault(os.getcwd())
print("Initializing Architect...")
architect = StructureArchitect(vault)
print("Generating Proposal...")
try:
    proposal = architect.generate_proposal()
    print(f"Proposal Generated: {len(proposal['actions'])} actions")
except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()
