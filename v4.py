import chess 

class engine_v4():
  def __init__(self, board, ply):
    self.board = board
    self.ply = ply
    self.cor = self.board.turn
    self.pv = {}

  def is_check_move(self,board,move):
      board.push(move)
      is_check = board.is_check()
      board.pop()
      return is_check

  def forced_mate_search(self,ply,board,cor):
    if board.is_checkmate():
        if board.turn != cor:
          return True
    if ply == 0 :
      return False
    oponnent_mated = 0
    oponnent_not_mated = 0
    turn_mate = 0
    for move in list(board.legal_moves):

        if board.turn == cor:
          if self.is_check_move(board,move):
            ms = board.copy()
            ms.push(move)
            if self.forced_mate_search(ply-1,ms,cor):
              turn_mate+=1
        else:
          ms = board.copy()
          ms.push(move)
          if self.forced_mate_search(ply-1,ms,cor):
            oponnent_mated+=1
          else:
            oponnent_not_mated+=1
        if oponnent_not_mated == 0 and turn_mate > 0:
          return True
    return False

  def forced_mated_search(self,ply,board,cor):
    if board.is_checkmate():
        if board.turn == cor:
          return True
    if ply == 0 :
      return False

    for move in list(board.legal_moves):
        if board.turn != cor:
          if self.is_check_move(board,move):
            ms = board.copy()
            ms.push(move)
            if self.forced_mate_search(ply-1,ms,cor):
              return True
        else:
          ms = board.copy()
          ms.push(move)
          if self.forced_mate_search(ply-1,ms,cor):
            return True
    return False

  def is_ending(self):
      queens = 0
      minors = 0

      queens+= len(self.board.pieces(chess.QUEEN,True))
      queens+= len(self.board.pieces(chess.QUEEN,True))

      pecas = [chess.ROOK, chess.BISHOP, chess.QUEEN]

      for peca in pecas:
        minors += len(self.board.pieces(peca,True))
        minors += len(self.board.pieces(peca,False))

      if queens == 0 or (queens == 2 and minors <= 1):
        return True

      return False



  def Piece_Square_Table(self, color):
    pawntable = [
        0, 0, 0, 0, 0, 0, 0, 0,
        5, 10, 10, -40, -40, 10, 10, 5,
        5, -5, -10, 0, 0, -10, -5, 5,
        0, 0, 0, 50, 50, 0, 0, 0,
        5, 5, 10, 25, 25, 10, 5, 5,
        10, 10, 20, 30, 30, 20, 10, 10,
        50, 50, 50, 50, 50, 50, 50, 50,
        0, 0, 0, 0, 0, 0, 0, 0]

    knightstable = [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20, 0, 5, 5, 0, -20, -40,
        -30, 5, 10, 15, 15, 10, 5, -30,
        -30, 0, 15, 20, 20, 15, 0, -30,
        -30, 5, 15, 20, 20, 15, 5, -30,
        -30, 0, 10, 15, 15, 10, 0, -30,
        -40, -20, 0, 0, 0, 0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50]

    bishopstable = [
        -20, -10, -40, -10, -10, -40, -10, -20,
        -10, 5, 0, 0, 0, 0, 5, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10, 0, 20, 10, 10, 20, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -20, -10, -40, -10, -10, -40, -10, -20]

    rookstable = [
        0, 0, 0, 5, 5, 0, 0, 0,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        5, 10, 10, 10, 10, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0]

    queenstable = [
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -10, 5, 5, 5, 5, 5, 0, -10,
        0, 0, 5, 5, 5, 5, 0, -5,
        -5, 0, 5, 5, 5, 5, 0, -5,
        -10, 0, 5, 5, 5, 5, 0, -10,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20]

    if self.is_ending():
      kingstable = [
    50, -30, -30, -30, -30, -30, -30, -50,
    -30, -30,  0,  0,  0,  0, -30, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 30, 40, 40, 30, -10, -30,
    -30, -10, 20, 30, 30, 20, -10, -30,
    -30, -20, -10,  0,  0, -10, -20, -30,
    -50, -40, -30, -20, -20, -30, -40, -50
]
    else:
      kingstable = [
          20, 30, 10, 0, 0, 10, 30, 20,
          20, 20, -10, -10, -10, -10, 20, 20,
          -10, -20, -20, -20, -20, -20, -20, -10,
          -20, -30, -30, -40, -40, -30, -30, -20,
          -30, -40, -40, -50, -50, -40, -40, -30,
          -30, -40, -40, -50, -50, -40, -40, -30,
          -30, -40, -40, -50, -50, -40, -40, -30,
          -30, -40, -40, -50, -50, -40, -40, -30]


    pecas = {chess.PAWN:pawntable, chess.ROOK:rookstable, chess.BISHOP:bishopstable,chess.KNIGHT:knightstable, chess.QUEEN:queenstable, chess.KING:kingstable}
    pecas_indx = {chess.PAWN:0, chess.ROOK:1, chess.BISHOP:2,chess.KNIGHT:3, chess.QUEEN:4, chess.KING:5}
    pecas_w = [0,0,0,0,0,0]
    pecas_b = [0,0,0,0,0,0]

    for peca in pecas:
       for i in self.board.pieces(peca, color):
          pecas_w[pecas_indx[peca]] += pecas[peca][i]

    for peca in pecas:
       for i in self.board.pieces(peca, not color):
          pecas_b[pecas_indx[peca]] -= pecas[peca][chess.square_mirror(i)]

    score = sum([i + b for i,b in zip(pecas_w,pecas_b)])

    return score

  def avaliacao(self,cor):
    if self.board.is_repetition(2):
      return 0
    score = 0
    pecas = {chess.PAWN:100, chess.ROOK:500,
    chess.BISHOP:300.15,chess.KNIGHT:300,
    chess.QUEEN:1000}

    for peca, valor in pecas.items():
      score += len(self.board.pieces(peca,cor)) * valor
      score -= len(self.board.pieces(peca, not cor)) * valor

    score += self.Piece_Square_Table(self.board.turn)
    return score


  def negamax(self, alpha, beta, ply):
    if self.board.is_checkmate():
        if self.board.turn == self.cor:
          return +9999
        else:
          return -9999
    if ply == 0:
      return self.avaliacao(self.board.turn)

    score = 0
    best_value = -1000

    if ply >= 3 and not self.board.is_check():
      self.board.push(chess.Move.null())
      score = -self.negamax(-beta,-beta+1,ply-3)
      self.board.pop()

      if score >= beta:
        return score

    for move in list(self.board.legal_moves):
      self.board.push(move)
      score = -self.negamax(-beta, -alpha, ply-1)

      self.board.pop()

      if score == 9999:
        return score

      if best_value < score:
        best_value = score

      if score >= beta:
        return beta

      alpha = max(score, alpha)

    return best_value

  def quisce(self,alpha,beta,ply):
    if ply == 0:
      return self.avaliacao(self.board.turn)

    stand_pat = self.avaliacao(self.board.turn)
    if stand_pat >= beta:
      return beta

    delta = 1000

    if alpha < stand_pat:
      alpha = stand_pat

    for move in list(self.board.legal_moves):
      if self.board.is_capture(move):
        self.board.push(move)
        score = -self.quisce(-beta, -alpha, ply-1)
        self.board.pop()

        if move.promotion:
            delta+=750
        if stand_pat < alpha-delta:
            return alpha
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    return alpha

  def check_move(self,ply):
    if self.board.is_checkmate():
        if self.board.turn == self.cor:
          return +9999
        else:
          return -9999
    if ply == 0:
      return self.avaliacao(self.board.turn)

    score = 0

    best_value = -1000
    for move in list(self.board.legal_moves):
      #print("Candidate: ",move)
      self.board.push(move)
      score = -self.check_move(ply-1)
      self.board.pop()
      # print(f"-----Depth {ply} -----")
      # print(move," : ",score)
      if score == 9999:
        return score

      if best_value < score:
        best_value = score


    return best_value


  def movement(self, depth):
    best_move = None
    best_value = -1000

    alpha = -1000
    beta = 1000

    for move in list(self.board.legal_moves):
      if self.is_check_move(self.board,move):
        bird = self.board.copy()
        cor = bird.turn
        bird.push(move)
        if self.forced_mate_search(2,bird, cor):
          return move

    # Checks if is getting mated
    possible_mated = []
    for move in list(self.board.legal_moves):
        bird = self.board.copy()
        bird.push(move)
        if self.forced_mated_search(2,bird, bird.turn):
          possible_mated.append(move)


    for ply in range(0,depth):
      sorted_moves = []
      if ply == 0:
        for move in list(self.board.legal_moves):
          self.board.push(move)
          if move in possible_mated:
            score = -9999

          elif self.board.is_repetition(2):
            score = -9999

          else:
            score = -self.negamax(-beta, -alpha, ply)
          self.board.pop()

          if best_move == None:
            best_move = move
            best_value = score

          if best_value < score:
            best_value = score
            best_move = move

          sorted_moves.append((move,score))
        sorted_moves = sorted(sorted_moves,key= lambda x: x[1],reverse=True)
        self.pv[ply] = sorted_moves
      else:
        for move in self.pv[ply-1]:
          self.board.push(move[0])
          if move[0] in possible_mated:
            score = -9999

          elif self.board.is_repetition(2):
            score = 0

          else:
            score = -self.negamax(-beta, -alpha, ply)
          self.board.pop()

          if best_move == None:
            best_move = move[0]
            best_value = score

          if best_value < score:
            best_value = score
            best_move = move[0]

          sorted_moves.append((move[0],score))
        sorted_moves = sorted(sorted_moves,key= lambda x: x[1],reverse=True)
        self.pv[ply] = sorted_moves



    return self.pv[ply][0][0]