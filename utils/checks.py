# utils/checks.py
DEVELOPER_ID = 1105948117624434728

def is_developer(interaction) -> bool:
    return interaction.user.id == DEVELOPER_ID
