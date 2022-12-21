from ..config.essemble_code import HAS_BARRIER
from ..config.essemble_code import NO_BARRIER
from ..config.automatic_code import LEFT
from ..config.automatic_code import RIGHT
from ..config.automatic_code import FORWARD
from ..config.automatic_code import SPECIFIC_HANDLE
######
######
# Thuyền rẽ khi nào
def only_lake(barriers):
  __, forward, right = barriers
  # Cả hai cảm biến đều có vật cản
  if right == HAS_BARRIER and forward == HAS_BARRIER:
    return SPECIFIC_HANDLE
  # Nếu cảm biến vật cản là có thì tiếp tục đi thẳng
  if right == HAS_BARRIER:
    return FORWARD
  # Nếu cảm biến vật cản là không thì rẽ phải
  if right == NO_BARRIER:
    return SPECIFIC_HANDLE
  if forward == HAS_BARRIER:
    return LEFT
    