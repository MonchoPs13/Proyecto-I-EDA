import curses, sys

def edit(stdscr):
  screen = curses.initscr()
  screen.nodelay(1)
  curses.noecho()
  curses.raw()
  screen.keypad(1)
  
  buffer = []
  src = 'noname.txt'
  rows, columns = screen.getmaxyx()
  xOffset, yOffset, currRow, currCol = [0] * 4
  
  if len(sys.argv) == 2: 
    src = sys.argv[1]

  try:
    with open(sys.argv[1]) as file:
      content = file.read().split('\n')
      content = content[:-1] if len(content) > 1 else content
      # popoulate buffer
      for row in content:
        # convert every character to its ascii value
        buffer.append([ord(char) for char in row])
  except:
    buffer.append([])
    
  if len(sys.argv) == 1: 
    buffer.append([])
    
  # MAIN LOOP
  while True:
    screen.move(0, 0)
    # scroll
    if currRow < yOffset:
      yOffset = currRow
    if currRow >= yOffset + rows:
      yOffset = currRow - rows + 1
    
    if currCol < xOffset:
      xOffset = currCol
    if currCol >= xOffset + columns:
      xOffset = currCol - columns + 1
      
    for row in range(rows):
      bufferRow = row + yOffset
      for col in range(columns):
        bufferCol = col + xOffset
        try:
          screen.addch(row, col, buffer[bufferRow][bufferCol])
        except:
          pass
      screen.clrtoeol()
      try:
        screen.addch('\n')
      except:
        pass
    
    curses.curs_set(0)
    screen.move(currRow - yOffset, currCol - xOffset)
    curses.curs_set(1)
    screen.refresh()
    ch = -1
    while ch == -1:
      ch = screen.getch()
      
    if ch != ((ch) & 0x1f) and ch < 128:
      buffer[currRow].insert(currCol, ch)
      currCol += 1
    elif chr(ch) in '\n\r':
      line = buffer[currRow][currCol:]
      buffer[currRow] = buffer[currRow][:currCol]
      currRow += 1
      currCol = 0
      buffer.insert(currRow, [] + line)
    elif ch == 8:
      # borrar
      if currCol:
        currCol -= 1
        del buffer[currRow][currCol]
      elif currRow:
        line = buffer[currRow][currCol:]
        del buffer[currRow]
        currRow -= 1
        currCol = len(buffer[currRow])
        buffer[currRow] += line
    elif ch == curses.KEY_LEFT:
      if currCol != 0:
        currCol -= 1
      elif currRow > 0:
        currRow -= 1
        currCol = len(buffer[currRow])
    elif ch == curses.KEY_RIGHT:
      if currCol < len(buffer[currRow]):
        currCol += 1
      elif currRow < len(buffer) - 1:
        currRow += 1
        currCol = 0
    elif ch == curses.KEY_UP and currRow != 0:
      currRow -= 1
    elif ch == curses.KEY_DOWN and currRow < len(buffer) - 1:
      currRow += 1
    
    row = buffer[currRow] if currRow < len(buffer) else None
    rowLen = len(row) if row is not None else 0
    if currCol > rowLen:
      currCol = rowLen
    
    # comandos del programa
    if ch == (ord('q') & 0x1f):
      sys.exit()
    elif ch == (ord('s') & 0x1f):
      content = ''
      for line in buffer:
        content += ''.join([chr(c) for c in line]) + '\n'
      with open(src, 'w') as file:
        file.write(content)
    
  
    
curses.wrapper(edit)