import json, os, sys, urllib.request

E=os.environ.get("MAKEFUN_ENV_URL")or sys.exit("NO_ENV")
V={"P":100,"N":320,"B":330,"R":500,"Q":900,"K":20000,"p":100,"n":320,"b":330,"r":500,"q":900,"k":20000}

def post(p, b):
    req = urllib.request.Request(E+p, data=json.dumps(b).encode(), headers={"content-type": "application/json"})
    with urllib.request.urlopen(req) as r: return json.load(r)

def board_of(fen):
    b = {}
    for i, row in enumerate(fen.split()[0].split("/")):
        f = 0
        for c in row:
            if c.isdigit(): f += int(c)
            else: b["abcdefgh"[f] + str(8-i)] = c; f += 1
    return b

def evaluate(board, is_white):
    score = 0
    for sq, p in board.items():
        v = V[p]
        f = ord(sq[0]) - 97
        r = int(sq[1]) - 1
        # Center control and piece activity
        center = 10 if 2 <= f <= 5 and 2 <= r <= 5 else 0
        if p.isupper():
            score += v + center
            if p == 'P': score += r * 5
        else:
            score -= v + center
            if p == 'p': score += (7 - r) * 5
    return score if is_white else -score

def choose(fen, legal):
    parts = fen.split()
    is_white = parts[1] == 'w'
    board = board_of(fen)
    
    best_score = -999999
    best_move = legal[0]
    
    for m in legal:
        src, dst = m[:2], m[2:4]
        b = board.copy()
        piece = b.pop(src, None)
        promo = m[4] if len(m) == 5 else None
        if promo:
            piece = promo.upper() if is_white else promo.lower()
        if piece and piece.lower() == 'p' and src[0] != dst[0] and dst not in b:
            b.pop(dst[0] + src[1], None)
        victim = b.get(dst)
        b[dst] = piece
        
        score = evaluate(b, is_white)
        # Bonus for captures and promotions
        if victim:
            score += V[victim] * 2
        if promo:
            score += 800
        
        if score > best_score:
            best_score = score
            best_move = m
            
    return best_move

while True:
    g = post("/game", {})
    if g["status"] == "done": break
    while g["status"] == "your_move":
        g = post("/move", {"game": g["game"], "move": choose(g["fen"], g["legal_moves"])})
    print(f"game {g['game']}: {g['outcome']}", file=sys.stderr)
print("done", file=sys.stderr)
