from src.config.essemble_code import END_PACKAGE

def standard(commands) -> str:
  r = commands.replace('\r', '') \
    .replace('\n', '')
  r = r.split(END_PACKAGE)
  return r