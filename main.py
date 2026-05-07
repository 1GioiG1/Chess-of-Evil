"""
Шахматы Зла / Chess of Evil
Pygame desktop application — full rewrite with bug fixes
"""

import pygame
import sys
import random
import os
import copy

pygame.init()
pygame.font.init()

def resource_path(rel):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, rel)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), rel)

LANG = "ru"

STRINGS = {
    "ru": {
        "title": "Шахматы Зла",
        "tab_game": "Игра",
        "tab_settings": "Настройки",
        "tab_learn": "Обучение",
        "new_game": "Новая игра",
        "roll_dice": "Бросить 2к6",
        "end_turn": "Завершить ход",
        "settings_title": "Настройки игры",
        "cost_move": "Ход",
        "cost_res": "Воскрешение",
        "res_count": "Раз",
        "max_actions": "Макс. действий за ход",
        "crit_bonus": "ОД при крите (12)",
        "fail_penalty": "Штраф при неудаче (2)",
        "castle_cost_lbl": "Стоимость рокировки",
        "save_settings": "Сохранить",
        "reset_settings": "Сбросить",
        "global_settings": "Глобальные настройки",
        "piece_settings": "Настройки фигур",
        "col_move_hint": "Сколько ОД стоит ход этой фигурой",
        "col_res_hint": "Сколько ОД стоит воскресить эту фигуру в фазе «Столкновение Судеб»",
        "col_count_hint": "Сколько раз за игру можно воскресить (∞ = без ограничений, 0 = нельзя)",
        "hint_max_actions": "Сколько раз за ход можно двигать фигуры (независимо от ОД)",
        "hint_crit": "Сумма ОД при броске 12. По умолчанию = 12",
        "hint_fail": "Сколько ОД теряется при броске 2. По умолчанию = 1",
        "hint_castle": "Стоимость рокировки в ОД (обычно = стоимость ладьи)",
        "allow_ep": "Взятие на проходе",
        "hint_ep": "Разрешить взятие пешки, прошедшей 2 клетки, соседней пешкой противника",
        "settings_locked": "Настройки заблокированы во время игры",
        "settings_lock_hint": "Начните новую игру, чтобы изменить настройки",
        "pieces": {"K":"Король","Q":"Ферзь","R":"Ладья","B":"Слон","N":"Конь","P":"Пешка"},
        "white": "Белые",
        "black": "Чёрные",
        "phase_normal": "Обычный ход",
        "phase_gambit": "Королевский Гамбит",
        "phase_clash": "Столкновение Судеб",
        "check": "ШАХ!",
        "checkmate": "МАТ!",
        "stalemate": "ПАТ — Ничья!",
        "winner": "{} побеждают!",
        "draw": "Ничья!",
        "ap_label": "ОД",
        "actions_label": "Ходов: {}/{}",
        "crit_msg": "Критическая удача! Двойной ход одной фигуры.",
        "fail_msg": "Критическая неудача! Штраф к ОД.",
        "roll_prompt": "Бросьте кубики",
        "choose_promo": "Выберите фигуру",
        "resurrect": "Воскрешение",
        "log_title": "Журнал",
        "log_takes": "{} берёт {}",
        "log_move": "{} → {}",
        "log_castle": "рокировка",
        "log_ep": "на проходе",
        "log_promo": "Превращение → {}",
        "log_res": "Воскрешение: {} → {}",
        "log_newgame": "Новая игра! Ход белых.",
        "log_turn": "Ход {}. Бросьте кубики.",
        "learn_next": "Далее →",
        "learn_prev": "← Назад",
        "learn_exit": "Готово",
        "unlimited": "∞",
    },
    "en": {
        "title": "Chess of Evil",
        "tab_game": "Game",
        "tab_settings": "Settings",
        "tab_learn": "Tutorial",
        "new_game": "New Game",
        "roll_dice": "Roll 2d6",
        "end_turn": "End Turn",
        "settings_title": "Game Settings",
        "cost_move": "Move",
        "cost_res": "Resurrect",
        "res_count": "Times",
        "max_actions": "Max Actions/Turn",
        "crit_bonus": "AP on Crit (12)",
        "fail_penalty": "Fail Penalty (2)",
        "castle_cost_lbl": "Castling Cost",
        "save_settings": "Save",
        "reset_settings": "Reset",
        "global_settings": "Global Settings",
        "piece_settings": "Piece Settings",
        "col_move_hint": "AP cost to move this piece",
        "col_res_hint": "AP cost to resurrect this piece in Clash of Fates phase",
        "col_count_hint": "How many times per game this piece can be resurrected (∞ = unlimited, 0 = never)",
        "hint_max_actions": "How many piece moves allowed per turn (regardless of AP)",
        "hint_crit": "AP gained when rolling 12. Default = 12",
        "hint_fail": "AP lost when rolling 2. Default = 1",
        "hint_castle": "AP cost of castling move (usually = rook cost)",
        "allow_ep": "En Passant",
        "hint_ep": "Allow capturing a pawn that just moved 2 squares by an adjacent enemy pawn",
        "settings_locked": "Settings are locked during a game",
        "settings_lock_hint": "Start a new game to change settings",
        "pieces": {"K":"King","Q":"Queen","R":"Rook","B":"Bishop","N":"Knight","P":"Pawn"},
        "white": "White",
        "black": "Black",
        "phase_normal": "Normal Turn",
        "phase_gambit": "Royal Gambit",
        "phase_clash": "Clash of Fates",
        "check": "CHECK!",
        "checkmate": "CHECKMATE!",
        "stalemate": "STALEMATE — Draw!",
        "winner": "{} win!",
        "draw": "Draw!",
        "ap_label": "AP",
        "actions_label": "Moves: {}/{}",
        "crit_msg": "Critical Hit! One piece may move twice.",
        "fail_msg": "Critical Fail! AP penalty.",
        "roll_prompt": "Roll the dice",
        "choose_promo": "Choose a piece",
        "resurrect": "Resurrect",
        "log_title": "Log",
        "log_takes": "{} takes {}",
        "log_move": "{} → {}",
        "log_castle": "castling",
        "log_ep": "en passant",
        "log_promo": "Promotion → {}",
        "log_res": "Resurrect: {} → {}",
        "log_newgame": "New game! White's turn.",
        "log_turn": "{}'s turn. Roll dice.",
        "learn_next": "Next →",
        "learn_prev": "← Back",
        "learn_exit": "Done",
        "unlimited": "∞",
    }
}

def T(key, *args):
    s = STRINGS[LANG].get(key, key)
    if args:
        s = s.format(*args)
    return s

def TP(key):
    return STRINGS[LANG]["pieces"].get(key, key)

C = {
    "bg": (18,18,24), "bg2": (28,28,36), "bg3": (38,38,50),
    "border": (60,60,80), "border2": (80,80,110),
    "text": (230,230,240), "text2": (160,160,180), "text3": (100,100,120),
    "accent": (90,140,220), "accent2": (60,100,180),
    "red": (200,60,60), "red2": (240,80,80),
    "gold": (210,170,60), "gold2": (240,200,80),
    "sq_light": (240,217,181), "sq_dark": (181,136,99),
    "sq_sel": (90,140,220), "sq_can": (90,180,90),
    "sq_cap": (200,80,80), "sq_check": (220,60,60),
    "panel": (24,24,32), "panel2": (32,32,44),
    "btn": (40,40,56), "btn_hover": (55,55,75),
    "btn_dis": (30,30,40),
    "die_bg": (35,35,50), "die_crit": (40,100,40), "die_fail": (120,30,30),
    "tab_active": (50,80,160),
    "inp_bg": (30,30,44), "inp_border": (70,70,100),
    "piece_w": (245,245,250), "piece_b": (15,15,20),
    "piece_w_outline": (20,20,30), "piece_b_outline": (210,210,220),
}

DEFAULT_SETTINGS = {
    "move_cost":   {"K":8,"Q":6,"R":5,"B":3,"N":3,"P":1},
    "res_cost":    {"K":8,"Q":6,"R":5,"B":3,"N":3,"P":1},
    "res_count":   {"K":0,"Q":1,"R":-1,"B":-1,"N":-1,"P":0},
    "max_actions": 3,
    "crit_ap":     12,
    "fail_penalty": 1,
    "castle_cost": 5,
    "allow_ep":    True,   # En passant toggle
}
settings = copy.deepcopy(DEFAULT_SETTINGS)


PIECE_GLYPH = {"K":"♚","Q":"♛","R":"♜","B":"♝","N":"♞","P":"♟"}
PIECE_TYPES = ["K","Q","R","B","N","P"]

def is_white(p): return p and p == p.upper()
def tp(p): return p.upper() if p else None
def pc(p): return "W" if is_white(p) else "B"
def opp(c): return "B" if c == "W" else "W"
def in_b(r,c): return 0 <= r < 8 and 0 <= c < 8
def f2l(c): return chr(97+c)
def coord_str(r,c): return f"{f2l(c)}{8-r}"

def raw_moves(board, r, c, ep, castling, skip_castle=False):
    p = board[r][c]
    if not p: return []
    t = tp(p); mine = pc(p); enemy = opp(mine)
    dir_ = -1 if is_white(p) else 1
    moves = []

    def push(tr, tc, sp=None):
        if not in_b(tr, tc): return False
        tgt = board[tr][tc]
        if tgt and pc(tgt) == mine: return False
        moves.append((tr, tc, sp))
        return not tgt

    def slide(dr, dc):
        rr, cc = r+dr, c+dc
        while in_b(rr, cc):
            if not push(rr, cc): break
            rr += dr; cc += dc

    if t == "P":
        if in_b(r+dir_, c) and not board[r+dir_][c]:
            moves.append((r+dir_, c, None))
            start = 6 if is_white(p) else 1
            if r == start and in_b(r+2*dir_, c) and not board[r+2*dir_][c]:
                moves.append((r+2*dir_, c, None))
        for dc in (-1, 1):
            nr, nc = r+dir_, c+dc
            if not in_b(nr, nc): continue
            tgt = board[nr][nc]
            if tgt and pc(tgt) == enemy:
                moves.append((nr, nc, None))
            elif ep and ep == (nr, nc) and settings.get("allow_ep", True):
                # Verify the pawn that passed is actually an enemy pawn on the adjacent square
                ep_pawn_r = r  # the enemy pawn is on the same row as us, adjacent column
                ep_pawn = board[ep_pawn_r][nc]
                if ep_pawn and tp(ep_pawn) == "P" and pc(ep_pawn) == enemy:
                    moves.append((nr, nc, "ep"))

    if t == "N":
        for dr,dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
            push(r+dr, c+dc)
    if t in ("B","Q"):
        for dr,dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
            slide(dr, dc)
    if t in ("R","Q"):
        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            slide(dr, dc)
    if t == "K":
        for dr,dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            push(r+dr, c+dc)
        if not skip_castle:
            row = 7 if is_white(p) else 0
            cr = castling[mine]
            if cr["k"] and not board[row][5] and not board[row][6] \
               and tp(board[row][7]) == "R" and pc(board[row][7]) == mine:
                moves.append((row, 6, "ck"))
            if cr["q"] and not board[row][3] and not board[row][2] \
               and not board[row][1] and tp(board[row][0]) == "R" and pc(board[row][0]) == mine:
                moves.append((row, 2, "cq"))
    return moves

def attacked_by(board, r, c, by_color, ep, castling):
    for rr in range(8):
        for cc in range(8):
            p = board[rr][cc]
            if p and pc(p) == by_color:
                if any(mr == r and mc == c for mr, mc, _ in raw_moves(board, rr, cc, ep, castling, True)):
                    return True
    return False

def king_pos(board, color):
    for r in range(8):
        for c in range(8):
            if tp(board[r][c]) == "K" and pc(board[r][c]) == color:
                return (r, c)
    return None

def in_check(board, color, ep, castling):
    kp = king_pos(board, color)
    if not kp: return False
    return attacked_by(board, kp[0], kp[1], opp(color), ep, castling)

def apply_raw(board, fr, fc, tr, tc, sp):
    b = [row[:] for row in board]
    p = b[fr][fc]
    captured = b[tr][tc]
    b[tr][tc] = p; b[fr][fc] = None
    if sp == "ep":
        er = tr+1 if is_white(p) else tr-1
        captured = b[er][tc]; b[er][tc] = None
    if sp == "ck": b[tr][5] = b[tr][7]; b[tr][7] = None
    if sp == "cq": b[tr][3] = b[tr][0]; b[tr][0] = None
    return b, captured

def legal_moves_for(board, r, c, ep, castling, color):
    p = board[r][c]
    if not p or pc(p) != color: return []
    result = []
    for tr, tc, sp in raw_moves(board, r, c, ep, castling):
        if sp in ("ck","cq"):
            mid_c = 5 if sp == "ck" else 3
            tmp = [row[:] for row in board]; tmp[r][c] = None
            if in_check(tmp, color, ep, castling): continue
            tmp2 = [row[:] for row in board]; tmp2[r][mid_c] = p; tmp2[r][c] = None
            if in_check(tmp2, color, ep, castling): continue
        b2, _ = apply_raw(board, r, c, tr, tc, sp)
        if not in_check(b2, color, ep, castling):
            result.append((tr, tc, sp))
    return result

def has_any_legal(board, color, ep, castling):
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p and pc(p) == color and legal_moves_for(board, r, c, ep, castling, color):
                return True
    return False

def all_pieces(board):
    return [(board[r][c], r, c) for r in range(8) for c in range(8) if board[r][c]]

def fresh_board():
    board = [[None]*8 for _ in range(8)]
    for c, p in enumerate("RNBQKBNR"):
        board[0][c] = p.lower()
        board[7][c] = p
    for c in range(8):
        board[1][c] = "p"; board[6][c] = "P"
    return board


class GameState:
    def __init__(self):
        self.board = fresh_board()
        self.turn = "W"
        self.od = {"W":0,"B":0}
        self.rolled = False
        self.act_used = 0
        self.moved_pieces = {}
        self.crit = False; self.crit_key = None; self.crit_used = False
        self.phase = "normal"
        self.castling = {"W":{"k":True,"q":True},"B":{"k":True,"q":True}}
        self.ep = None
        self.dead = {"W":[],"B":[]}
        self.res_counts = {"W":{},"B":{}}
        self.sel = None; self.legal = []
        self.over = False; self.winner = None
        self.promo_at = None
        self.check_sq = None
        self.log = []
        self.dice = (0, 0)
        self._clash_triggered = False
        self.game_started = False   # becomes True after first piece move


    def add_log(self, msg, color="sys"):
        self.log.insert(0, (msg, color))
        if len(self.log) > 60:
            self.log.pop()

    def detect_phase(self):
        pieces = all_pieces(self.board)
        w_nk = [x for x in pieces if pc(x[0]) == "W" and tp(x[0]) != "K"]
        b_nk = [x for x in pieces if pc(x[0]) == "B" and tp(x[0]) != "K"]
        # Clash of Fates: once both sides reach kings-only, stay in clash forever
        # (even if pieces are resurrected back onto the board)
        if not w_nk and not b_nk:
            self._clash_triggered = True
        if getattr(self, "_clash_triggered", False):
            return "clash"
        active_nk = w_nk if self.turn == "W" else b_nk
        if not active_nk: return "gambit"
        return "normal"

    def move_cost(self, p, r, c):
        t = tp(p); color = pc(p)
        if t == "K":
            if in_check(self.board, color, self.ep, self.castling):
                return self.od[color]
            if self.phase == "gambit" and color == self.turn:
                return 1
            return settings["move_cost"]["K"]
        return settings["move_cost"][t]

    def piece_key(self, r, c):
        return r * 8 + c

    def times_moved(self, r, c):
        return self.moved_pieces.get(self.piece_key(r, c), 0)

    def can_select(self, r, c):
        if not self.rolled or self.over or self.promo_at: return False
        if self.act_used >= settings["max_actions"]: return False
        p = self.board[r][c]
        if not p or pc(p) != self.turn: return False
        cost = self.move_cost(p, r, c)
        if self.od[self.turn] < cost: return False
        times = self.times_moved(r, c)
        if times >= 1:
            if not self.crit or self.crit_used: return False
            if self.crit_key is not None and self.crit_key != self.piece_key(r, c): return False
            if times >= 2: return False
        return bool(legal_moves_for(self.board, r, c, self.ep, self.castling, self.turn))

    def execute_move(self, fr, fc, tr, tc, sp):
        self.game_started = True   # lock settings from now on
        p = self.board[fr][fc]
        t = tp(p); color = self.turn
        cost = settings["castle_cost"] if sp in ("ck","cq") else self.move_cost(p, fr, fc)
        self.od[color] -= cost
        self.act_used += 1

        src_key = self.piece_key(fr, fc); dst_key = self.piece_key(tr, tc)
        src_times = self.moved_pieces.get(src_key, 0)
        self.moved_pieces.pop(src_key, None)
        self.moved_pieces[dst_key] = src_times + 1

        if self.crit and not self.crit_used:
            if src_times == 0:
                if self.crit_key is None: self.crit_key = dst_key
            else:
                if self.crit_key == dst_key: self.crit_used = True

        b2, captured = apply_raw(self.board, fr, fc, tr, tc, sp)
        self.board = b2

        self.ep = None
        if t == "P" and abs(tr - fr) == 2:
            self.ep = (fr + (1 if tr > fr else -1), fc)

        if t == "K":
            self.castling[color] = {"k":False,"q":False}
        if t == "R":
            if fc == 0: self.castling[color]["q"] = False
            if fc == 7: self.castling[color]["k"] = False
        if captured and tp(captured) == "R":
            ec = pc(captured)
            if tc == 0: self.castling[ec]["q"] = False
            if tc == 7: self.castling[ec]["k"] = False

        note = ""
        if sp in ("ck","cq"): note = f" ({T('log_castle')})"
        elif sp == "ep": note = f" ({T('log_ep')})"

        if captured:
            self.add_log(T("log_takes", PIECE_GLYPH[t], PIECE_GLYPH[tp(captured)]) + note, color)
            self.dead[pc(captured)].append(tp(captured))
        else:
            self.add_log(T("log_move", PIECE_GLYPH[t], coord_str(tr, tc)) + note, color)

        if t == "P" and (tr == 0 or tr == 7):
            self.promo_at = (tr, tc)
            return
        self.after_move()

    def after_move(self):
        self.sel = None; self.legal = []
        self.phase = self.detect_phase()
        enemy = opp(self.turn)
        kp = king_pos(self.board, enemy)
        self.check_sq = kp if in_check(self.board, enemy, self.ep, self.castling) else None

    def promote(self, piece_type):
        r, c = self.promo_at
        p = piece_type if self.turn == "W" else piece_type.lower()
        self.board[r][c] = p
        self.dead[self.turn].append("P")
        self.add_log(T("log_promo", PIECE_GLYPH[piece_type]), self.turn)
        self.promo_at = None
        self.after_move()

    def check_start_of_turn(self):
        color = self.turn
        chk = in_check(self.board, color, self.ep, self.castling)
        any_legal = has_any_legal(self.board, color, self.ep, self.castling)
        if chk and not any_legal:
            self.over = True; self.winner = opp(color)
            self.add_log(T("checkmate"), "sys")
            return False
        if not chk and not any_legal:
            self.over = True; self.winner = None
            self.add_log(T("stalemate"), "sys")
            return False
        self.check_sq = king_pos(self.board, color) if chk else None
        return True

    def roll(self):
        if self.rolled or self.over: return None, None
        d1 = random.randint(1, 6); d2 = random.randint(1, 6); s = d1 + d2
        self.dice = (d1, d2)
        self.crit = False; self.crit_key = None; self.crit_used = False
        if s == 12:
            self.crit = True
            self.od[self.turn] = settings["crit_ap"]
            self.add_log(T("crit_msg"), self.turn)
        elif s == 2:
            self.od[self.turn] = max(0, s - settings["fail_penalty"])
            self.add_log(T("fail_msg"), self.turn)
        else:
            self.od[self.turn] = s
            self.add_log(f"{T('white') if self.turn=='W' else T('black')}: {d1}+{d2}={s} {T('ap_label')}", self.turn)
        self.rolled = True; self.moved_pieces = {}; self.act_used = 0
        self.phase = self.detect_phase()
        self.check_start_of_turn()
        return d1, d2

    def end_turn(self):
        if not self.rolled or self.over: return
        # Reset CURRENT player's AP before switching
        self.od[self.turn] = 0
        self.turn = opp(self.turn)
        self.rolled = False; self.act_used = 0; self.moved_pieces = {}
        self.crit = False; self.crit_key = None; self.crit_used = False
        self.sel = None; self.legal = []; self.check_sq = None
        self.add_log(T("log_turn", T("white") if self.turn=="W" else T("black")), "sys")

    def get_resurrectable(self):
        if self.phase != "clash" or not self.rolled or self.over: return []
        if self.act_used >= settings["max_actions"]: return []
        seen = {}
        for t in self.dead[self.turn]:
            if t in seen: continue
            # Kings cannot be resurrected
            if t == "K": continue
            max_r = settings["res_count"].get(t, -1)
            if max_r == 0: continue
            used = self.res_counts[self.turn].get(t, 0)
            if max_r != -1 and used >= max_r: continue
            cost = settings["res_cost"].get(t, settings["move_cost"].get(t, 1))
            if self.od[self.turn] < cost: continue
            seen[t] = cost
        return list(seen.items())

    def resurrect(self, t):
        if self.act_used >= settings["max_actions"]: return
        cost = settings["res_cost"].get(t, settings["move_cost"].get(t, 1))
        if self.od[self.turn] < cost: return
        p = t if self.turn == "W" else t.lower()
        orig = self._orig_positions(p)
        placed = None
        for r, c in orig:
            if not self.board[r][c]:
                self.board[r][c] = p; placed = (r, c); break
        if not placed:
            br, bc = orig[0]
            cands = [(br+dr, bc+dc) for dr in range(-3,4) for dc in range(-3,4)
                     if in_b(br+dr, bc+dc) and not self.board[br+dr][bc+dc]]
            if cands:
                pick = random.choice(cands)
                self.board[pick[0]][pick[1]] = p
                placed = pick
        if not placed: return
        self.od[self.turn] -= cost; self.act_used += 1
        idx = self.dead[self.turn].index(t)
        self.dead[self.turn].pop(idx)
        self.res_counts[self.turn][t] = self.res_counts[self.turn].get(t, 0) + 1
        self.phase = self.detect_phase()
        self.add_log(T("log_res", PIECE_GLYPH[t], coord_str(placed[0], placed[1])), self.turn)

    def _orig_positions(self, p):
        t = tp(p); row = 7 if is_white(p) else 0
        pawn_row = 6 if is_white(p) else 1
        return {
            "K":[(row,4)],"Q":[(row,3)],
            "R":[(row,0),(row,7)],"B":[(row,2),(row,5)],
            "N":[(row,1),(row,6)],
            "P":[(pawn_row, c) for c in range(8)],
        }.get(t, [(row, 4)])


# ─────────────────────────────────────────
#  AI BOT
# ─────────────────────────────────────────

PIECE_VALUE = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
CENTER_BONUS = {
    (3,3):0.3,(3,4):0.3,(4,3):0.3,(4,4):0.3,
    (2,3):0.1,(2,4):0.1,(3,2):0.1,(3,5):0.1,
    (4,2):0.1,(4,5):0.1,(5,3):0.1,(5,4):0.1,
}

def _eval_board(board, color):
    """Simple material + position evaluation for `color`."""
    score = 0.0
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if not p: continue
            val = PIECE_VALUE.get(tp(p), 0)
            bonus = CENTER_BONUS.get((r, c), 0)
            # Pawn advancement bonus
            if tp(p) == "P":
                adv = (6 - r) if is_white(p) else (r - 1)
                bonus += adv * 0.05
            sign = 1 if pc(p) == color else -1
            score += sign * (val + bonus)
    return score

def bot_pick_move(gs, difficulty="medium"):
    """
    Returns (fr, fc, tr, tc, sp) or None.
    difficulty: "easy" | "medium" | "hard"
    """
    import random as _rnd

    color = gs.turn
    # Gather all legal moves for all affordable pieces
    candidates = []
    for r in range(8):
        for c in range(8):
            if gs.can_select(r, c):
                for mv in legal_moves_for(gs.board, r, c, gs.ep, gs.castling, color):
                    candidates.append((r, c) + mv)

    if not candidates:
        return None

    if difficulty == "easy":
        return _rnd.choice(candidates)

    # Score each candidate move
    def score_move(mv):
        fr, fc, tr, tc, sp = mv
        b2, cap = apply_raw(gs.board, fr, fc, tr, tc, sp)
        base = _eval_board(b2, color)
        # Penalise moving into danger
        if attacked_by(b2, tr, tc, opp(color), gs.ep, gs.castling):
            base -= PIECE_VALUE.get(tp(gs.board[fr][fc]), 0) * 0.8
        # Bonus for checks
        if in_check(b2, opp(color), gs.ep, gs.castling):
            base += 0.5
        return base

    scored = [(score_move(mv), mv) for mv in candidates]
    scored.sort(key=lambda x: -x[0])

    if difficulty == "medium":
        # Pick from top-3 randomly to add variation
        top = scored[:min(3, len(scored))]
        return _rnd.choice(top)[1]

    # Hard: deterministic best move (top-1 with tiny noise)
    noise = [(s + _rnd.uniform(0, 0.01), mv) for s, mv in scored]
    noise.sort(key=lambda x: -x[0])
    return noise[0][1]


# ─────────────────────────────────────────
#  LAN NETWORKING
# ─────────────────────────────────────────
import socket, threading, json as _json, queue as _queue

class NetworkRole:
    HOST = "host"
    CLIENT = "client"
    NONE = "none"

class LanSession:
    PORT = 47832
    MAGIC = b"COE1"

    def __init__(self):
        self.role = NetworkRole.NONE
        self.sock: socket.socket | None = None
        self.conn: socket.socket | None = None
        self.in_q: _queue.Queue = _queue.Queue()
        self.out_q: _queue.Queue = _queue.Queue()
        self.connected = False
        self.error: str = ""
        self.my_color: str = "W"   # host=W, client=B
        self._thread: threading.Thread | None = None

    def start_host(self):
        self.role = NetworkRole.HOST
        self.my_color = "W"
        self.error = ""
        self._thread = threading.Thread(target=self._host_thread, daemon=True)
        self._thread.start()

    def start_client(self, host_ip: str):
        self.role = NetworkRole.CLIENT
        self.my_color = "B"
        self.error = ""
        self._thread = threading.Thread(target=self._client_thread,
                                        args=(host_ip,), daemon=True)
        self._thread.start()

    def _host_thread(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(("", self.PORT))
            self.sock.listen(1)
            self.conn, _ = self.sock.accept()
            self.conn.send(self.MAGIC)
            self.connected = True
            self._io_loop(self.conn)
        except Exception as e:
            self.error = str(e)
            self.connected = False

    def _client_thread(self, host_ip):
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((host_ip, self.PORT))
            magic = self.conn.recv(4)
            if magic != self.MAGIC:
                raise ValueError("Bad magic")
            self.connected = True
            self._io_loop(self.conn)
        except Exception as e:
            self.error = str(e)
            self.connected = False

    def _io_loop(self, conn):
        conn.settimeout(0.05)
        buf = b""
        while True:
            # Send outgoing
            while not self.out_q.empty():
                msg = self.out_q.get_nowait()
                data = _json.dumps(msg).encode() + b"\n"
                try:
                    conn.sendall(data)
                except Exception:
                    self.connected = False; return
            # Receive incoming
            try:
                chunk = conn.recv(4096)
                if not chunk:
                    self.connected = False; return
                buf += chunk
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    try:
                        self.in_q.put(_json.loads(line))
                    except Exception:
                        pass
            except socket.timeout:
                pass
            except Exception:
                self.connected = False; return

    def send(self, msg: dict):
        self.out_q.put(msg)

    def poll(self) -> dict | None:
        if not self.in_q.empty():
            return self.in_q.get_nowait()
        return None

    def get_local_ip(self) -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def close(self):
        self.connected = False
        for s in [self.conn, self.sock]:
            if s:
                try: s.close()
                except Exception: pass
        self.conn = None; self.sock = None


FONTS = {}

def get_font_path():
    paths = [
        resource_path("assets/DejaVuSans.ttf"),
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/DejaVuSans.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for fp in paths:
        if os.path.exists(fp): return fp
    return None

def get_symbol_font_path():
    paths = [
        resource_path("assets/DejaVuSans.ttf"),
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/seguisym.ttf",
        "C:/Windows/Fonts/segoeuisymbol.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for fp in paths:
        if os.path.exists(fp): return fp
    return None

def load_fonts():
    global FONTS
    fp = get_font_path()
    def mf(size):
        if fp: return pygame.font.Font(fp, size)
        return pygame.font.SysFont("dejavusans,segoeui,arial", size)
    FONTS = {
        "big": mf(24), "med": mf(17), "sm": mf(14),
        "xs": mf(12), "coord": mf(10),
    }

def draw_rect(surf, color, rect, radius=6, border=0, border_color=None):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surf, border_color, rect, border, border_radius=radius)

def draw_text(surf, text, font, color, x, y, anchor="topleft"):
    s = font.render(text, True, color)
    r = s.get_rect()
    setattr(r, anchor, (int(x), int(y)))
    surf.blit(s, r)
    return r

def wrap_text(text, font, max_width):
    lines = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append(""); continue
        words = paragraph.split()
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if font.size(test)[0] <= max_width:
                cur = test
            else:
                if cur: lines.append(cur)
                cur = w
        if cur: lines.append(cur)
    return lines


_piece_cache = {}
_symbol_font_cache = {}

def piece_surface(piece_char, size):
    key = (piece_char, size)
    if key in _piece_cache:
        return _piece_cache[key]
    t = tp(piece_char)
    is_w = is_white(piece_char)

    # ── Try PNG pieces first (assets/pieces/<W|B><type>.png) ──
    png_path = resource_path(f"assets/pieces/{'W' if is_w else 'B'}{t}.png")
    if os.path.exists(png_path):
        try:
            img = pygame.image.load(png_path).convert_alpha()
            img = pygame.transform.smoothscale(img, (size, size))
            _piece_cache[key] = img
            return img
        except Exception:
            pass

    # ── Unicode glyph fallback ─────────────────────────────────
    glyph = PIECE_GLYPH[t]
    fill   = C["piece_w"] if is_w else C["piece_b"]
    outline = C["piece_w_outline"] if is_w else C["piece_b_outline"]

    if size not in _symbol_font_cache:
        sfp = get_symbol_font_path()
        if sfp:
            _symbol_font_cache[size] = pygame.font.Font(sfp, size)
        else:
            _symbol_font_cache[size] = pygame.font.SysFont("segoeuisymbol,dejavusans", size)
    font = _symbol_font_cache[size]

    pad = 3
    total = size + pad * 2 + 4
    surf = pygame.Surface((total, total), pygame.SRCALPHA)

    outline_surf = font.render(glyph, True, outline)
    fill_surf    = font.render(glyph, True, fill)

    # Centre the glyph properly in the surface
    gw, gh = fill_surf.get_size()
    ox = (total - gw) // 2
    oy = (total - gh) // 2

    for dx in range(-pad, pad + 1):
        for dy in range(-pad, pad + 1):
            if dx == 0 and dy == 0: continue
            surf.blit(outline_surf, (ox + dx, oy + dy))
    surf.blit(fill_surf, (ox, oy))

    _piece_cache[key] = surf
    return surf

def clear_piece_cache():
    _piece_cache.clear()
    _symbol_font_cache.clear()


# ─────────────────────────────────────────
#  ANIMATION SYSTEM
# ─────────────────────────────────────────
import time as _time

class PieceAnim:
    """Sliding piece animation from src to dst pixel coords."""
    DURATION = 0.18   # seconds

    def __init__(self, piece, sx, sy, ex, ey):
        self.piece = piece
        self.sx, self.sy = sx, sy
        self.ex, self.ey = ex, ey
        self.t0 = _time.monotonic()
        self.done = False

    def progress(self):
        t = (_time.monotonic() - self.t0) / self.DURATION
        t = min(1.0, t)
        # ease-out cubic
        t = 1 - (1 - t) ** 3
        return t

    def pos(self):
        p = self.progress()
        return (self.sx + (self.ex - self.sx) * p,
                self.sy + (self.ey - self.sy) * p)

    def is_done(self):
        return _time.monotonic() - self.t0 >= self.DURATION


def _ease_pulse(period=1.2):
    """0→1→0 sine pulse for selection glow."""
    t = _time.monotonic()
    return (math.sin(t * 2 * math.pi / period) + 1) / 2


import math

def draw_sq_highlight(surf, rect, color, alpha=160, radius=4):
    """Draw a coloured semi-transparent highlight over a square."""
    hl = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    hl.fill((*color, alpha))
    surf.blit(hl, rect.topleft)


def draw_board_frame(surf, bx, by, bsize, sq):
    """Draw decorative wooden-style border around the board."""
    frame = 14
    fr = pygame.Rect(bx - frame, by - frame, bsize + frame * 2, bsize + frame * 2)
    # Outer shadow
    shad = pygame.Surface((fr.width + 8, fr.height + 8), pygame.SRCALPHA)
    pygame.draw.rect(shad, (0, 0, 0, 90), (0, 0, fr.width + 8, fr.height + 8), border_radius=10)
    surf.blit(shad, (fr.x - 2, fr.y + 4))
    # Frame body – dark wood colour
    pygame.draw.rect(surf, (55, 38, 22), fr, border_radius=8)
    # Inner highlight stripe
    pygame.draw.rect(surf, (80, 55, 30), fr, 2, border_radius=8)
    # Coord labels inside frame
    font = FONTS["coord"]
    for c in range(8):
        lbl = f2l(c)
        cx = bx + c * sq + sq // 2
        draw_text(surf, lbl, font, (180, 140, 90), cx, by + bsize + 3, "midtop")
        draw_text(surf, lbl, font, (180, 140, 90), cx, by - frame + 1, "midtop")
    for r in range(8):
        lbl = str(8 - r)
        ry = by + r * sq + sq // 2
        draw_text(surf, lbl, font, (180, 140, 90), bx - frame + 2, ry, "midleft")
        draw_text(surf, lbl, font, (180, 140, 90), bx + bsize + 3, ry, "midleft")


def draw_piece_shadow(surf, cx, bottom_y, psize):
    """Draw a soft oval shadow at the bottom of a piece."""
    sw = int(psize * 0.65)
    sh = max(4, int(psize * 0.12))
    if sw < 4: return
    shad = pygame.Surface((sw + 4, sh + 4), pygame.SRCALPHA)
    pygame.draw.ellipse(shad, (0, 0, 0, 50), (2, 2, sw, sh))
    surf.blit(shad, (cx - sw // 2 - 2, bottom_y - sh))


class Button:
    def __init__(self, rect, label, font=None, color=None, hover_color=None,
                 text_color=None, disabled_color=None, radius=8):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.font = font or FONTS["med"]
        self.color = color or C["btn"]
        self.hover_color = hover_color or C["btn_hover"]
        self.text_color = text_color or C["text"]
        self.disabled_color = disabled_color or C["btn_dis"]
        self.radius = radius
        self.hovered = False
        self.disabled = False

    def draw(self, surf):
        if self.disabled: bg, tc = self.disabled_color, C["text3"]
        elif self.hovered: bg, tc = self.hover_color, self.text_color
        else: bg, tc = self.color, self.text_color
        draw_rect(surf, bg, self.rect, self.radius, 1, C["border"])
        s = self.font.render(self.label, True, tc)
        r = s.get_rect(center=self.rect.center)
        surf.blit(s, r)

    def update_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def clicked(self, event):
        if self.disabled: return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False


class Spinner:
    def __init__(self, rect, value, min_val, max_val, allow_unlimited=False):
        self.rect = pygame.Rect(rect)
        self.value = value; self.min_val = min_val; self.max_val = max_val
        self.allow_unlimited = allow_unlimited
        self._layout()

    def _layout(self):
        bw = 32  # fixed button width
        # Ensure there's at least 40px for the value in the middle
        min_total = bw * 2 + 40
        if self.rect.width < min_total:
            # Expand rect to fit
            extra = min_total - self.rect.width
            self.rect.inflate_ip(extra, 0)
        self.btn_minus = pygame.Rect(self.rect.x, self.rect.y, bw, self.rect.height)
        self.btn_plus  = pygame.Rect(self.rect.right - bw, self.rect.y, bw, self.rect.height)
        self.val_rect  = pygame.Rect(self.rect.x + bw + 2, self.rect.y,
                                     self.rect.width - 2 * bw - 4, self.rect.height)

    def set_rect(self, rect):
        self.rect = pygame.Rect(rect); self._layout()

    def draw(self, surf):
        draw_rect(surf, C["inp_bg"], self.rect, 6, 1, C["inp_border"])
        draw_rect(surf, C["btn"], self.btn_minus, 6)
        draw_rect(surf, C["btn"], self.btn_plus, 6)
        draw_text(surf, "−", FONTS["med"], C["text"],
                  self.btn_minus.centerx, self.btn_minus.centery, "center")
        draw_text(surf, "+", FONTS["med"], C["text"],
                  self.btn_plus.centerx, self.btn_plus.centery, "center")
        val_str = T("unlimited") if (self.allow_unlimited and self.value == -1) else str(self.value)
        draw_text(surf, val_str, FONTS["med"], C["text"],
                  self.val_rect.centerx, self.val_rect.centery, "center")

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_minus.collidepoint(event.pos):
                if self.value == -1:
                    self.value = self.max_val
                elif self.value > self.min_val:
                    self.value -= 1
                elif self.allow_unlimited and self.value == self.min_val:
                    self.value = -1
                return True
            if self.btn_plus.collidepoint(event.pos):
                if self.value == -1:
                    self.value = self.min_val
                elif self.value < self.max_val:
                    self.value += 1
                elif self.allow_unlimited and self.value == self.max_val:
                    self.value = -1
                return True
        return False


class Toggle:
    """ON/OFF toggle switch"""
    def __init__(self, x, y, value=True):
        self.value = value
        self.w, self.h = 48, 26
        self.rect = pygame.Rect(x, y, self.w, self.h)
        self.disabled = False

    def set_pos(self, x, y):
        self.rect = pygame.Rect(x, y, self.w, self.h)

    def draw(self, surf):
        if self.disabled:
            bg = C["bg3"] if not self.value else (40, 70, 40)
            knob_c = C["text3"]
        else:
            bg = C["accent2"] if self.value else C["bg3"]
            knob_c = C["text"] if self.value else C["text2"]
        pygame.draw.rect(surf, bg, self.rect, border_radius=13)
        pygame.draw.rect(surf, C["border2"], self.rect, 1, border_radius=13)
        knob_x = self.rect.right - 15 if self.value else self.rect.left + 3
        pygame.draw.circle(surf, knob_c, (knob_x + 7, self.rect.centery), 10)

    def handle(self, event):
        if self.disabled: return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.value = not self.value
                return True
        return False


DIE_DOTS = {
    1: [(0.5,0.5)],
    2: [(0.28,0.28),(0.72,0.72)],
    3: [(0.25,0.25),(0.5,0.5),(0.75,0.75)],
    4: [(0.28,0.28),(0.72,0.28),(0.28,0.72),(0.72,0.72)],
    5: [(0.25,0.25),(0.75,0.25),(0.5,0.5),(0.25,0.75),(0.75,0.75)],
    6: [(0.28,0.22),(0.72,0.22),(0.28,0.5),(0.72,0.5),(0.28,0.78),(0.72,0.78)],
}

def draw_die(surf, val, rect, crit=False, fail=False, player_color=None):
    if crit:
        bg = C["die_crit"]; border = (80,180,80)
        dot_color = (220,255,200)
    elif fail:
        bg = C["die_fail"]; border = (200,80,80)
        dot_color = (255,200,180)
    elif player_color == "W":
        # Clearly white die: ivory background, dark dots
        bg = (240, 235, 218); border = (180, 160, 120)
        dot_color = (40, 30, 20)
    elif player_color == "B":
        # Clearly black die: very dark background, light dots
        bg = (22, 18, 30); border = (130, 100, 180)
        dot_color = (220, 210, 240)
    else:
        bg = C["die_bg"]; border = C["border2"]
        dot_color = C["text"]
    draw_rect(surf, bg, rect, 8, 2, border)
    if val < 1 or val > 6:
        draw_text(surf, "?", FONTS["med"], C["text2"], rect.centerx, rect.centery, "center")
        return
    dot_r = max(3, rect.width // 10)

    # Inner shadow on top-left
    hl_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(hl_surf, (255,255,255,18), (1,1,rect.width-2,6), border_radius=6)
    surf.blit(hl_surf, rect.topleft)

    for fx, fy in DIE_DOTS[val]:
        cx = int(rect.x + fx * rect.width)
        cy = int(rect.y + fy * rect.height)
        # Subtle dot shadow
        pygame.draw.circle(surf, (0,0,0,60), (cx+1, cy+1), dot_r)
        pygame.draw.circle(surf, dot_color, (cx, cy), dot_r)
        # Tiny highlight on dot
        hi_c = tuple(min(255, v+60) for v in dot_color)
        pygame.draw.circle(surf, hi_c, (cx - dot_r//3, cy - dot_r//3), max(1, dot_r//3))


class SettingsScreen:
    def __init__(self):
        self.scroll_y = 0
        self.content_h = 0
        self.spinners_piece = {}
        self.spinners_global = {}
        self.locked = False
        self._flash = None    # ("save"|"reset", timestamp) for button flash
        self._build_widgets()

    def _build_widgets(self):
        self.spinners_piece = {}
        for t in PIECE_TYPES:
            self.spinners_piece[("move", t)] = Spinner((0,0,120,32), settings["move_cost"][t], 1, 30)
            self.spinners_piece[("res_cost", t)] = Spinner((0,0,120,32), settings["res_cost"][t], 1, 30)
            self.spinners_piece[("res_count", t)] = Spinner(
                (0,0,120,32), settings["res_count"][t], 0, 10, allow_unlimited=True)
        self.spinners_global = {
            "max_actions":  Spinner((0,0,120,32), settings["max_actions"], 1, 10),
            "crit_ap":      Spinner((0,0,120,32), settings["crit_ap"], 1, 30),
            "fail_penalty": Spinner((0,0,120,32), settings["fail_penalty"], 0, 5),
            "castle_cost":  Spinner((0,0,120,32), settings["castle_cost"], 1, 30),
        }
        self.ep_toggle = Toggle(0, 0, settings.get("allow_ep", True))
        self.btn_save = Button((0,0,160,40), T("save_settings"),
                                color=C["accent2"], hover_color=C["accent"])
        self.btn_reset = Button((0,0,160,40), T("reset_settings"))

    def _layout(self, w, h):
        self.surf_w = w; self.surf_h = h
        margin = 40
        max_w = min(860, w - 2 * margin)
        x_start = (w - max_w) // 2

        col_label = 140
        col_w = (max_w - col_label) // 3
        spinner_w = min(130, col_w - 28)

        self._x_label = x_start + 8
        self._spinner_w = spinner_w
        self._col_centers = [
            x_start + col_label + col_w // 2,
            x_start + col_label + col_w + col_w // 2,
            x_start + col_label + 2 * col_w + col_w // 2,
        ]
        self._x_start = x_start
        self._max_w = max_w

        y = 28
        self._title_y = y
        y += 54
        self._piece_header_y = y    # column titles start here
        header_block = 66           # title (18) + gap (6) + hint line1 (13) + hint line2 (13) + gap (16)
        y += header_block
        row_h = 50                  # 9px top gap + 32px spinner + 9px bottom

        for i, t in enumerate(PIECE_TYPES):
            ry = y + i * row_h + (row_h - 32) // 2
            for j, key_kind in enumerate(["move", "res_cost", "res_count"]):
                cx = self._col_centers[j]
                self.spinners_piece[(key_kind, t)].set_rect(
                    (cx - spinner_w // 2, ry, spinner_w, 32))
        y += len(PIECE_TYPES) * row_h + 28
        self._sep_y = y
        y += 22
        self._global_header_y = y
        y += 36

        x_global_label = x_start + 16
        x_global_spin = x_start + max_w - spinner_w - 16
        global_row_h = 64          # label (16) + hint (13) + gap (3) + spinner (32)
        for i, k in enumerate(["max_actions","crit_ap","fail_penalty","castle_cost"]):
            ry = y + i * global_row_h + 29
            self.spinners_global[k].set_rect((x_global_spin, ry, spinner_w, 32))
        self._x_global_label = x_global_label
        self._global_row_h = global_row_h
        y += 4 * global_row_h + 16

        # En passant toggle row
        self._ep_y = y
        self._ep_toggle_x = x_global_spin + spinner_w - self.ep_toggle.w
        self.ep_toggle.set_pos(self._ep_toggle_x, y + 28)
        y += global_row_h + 10

        btn_w = 160; btn_gap = 16
        total = 2 * btn_w + btn_gap
        bx = (w - total) // 2
        self.btn_save.rect = pygame.Rect(bx, y, btn_w, 40)
        self.btn_reset.rect = pygame.Rect(bx + btn_w + btn_gap, y, btn_w, 40)
        y += 65
        self.content_h = y
    def draw(self, surf):
        self._layout(surf.get_width(), surf.get_height())
        max_scroll = max(0, self.content_h - surf.get_height())
        self.scroll_y = max(0, min(self.scroll_y, max_scroll))

        content = pygame.Surface((surf.get_width(), max(self.content_h, surf.get_height())), pygame.SRCALPHA)
        content.fill(C["bg"])

        draw_text(content, T("settings_title"), FONTS["big"], C["text"],
                  surf.get_width() // 2, self._title_y, "midtop")

        draw_text(content, T("piece_settings"), FONTS["med"], C["text2"],
                  self._x_start + 10, self._piece_header_y - 28, "topleft")

        headers = [T("cost_move"), T("cost_res"), T("res_count")]
        hints = ["col_move_hint", "col_res_hint", "col_count_hint"]
        for i, (hdr, hint_key) in enumerate(zip(headers, hints)):
            draw_text(content, hdr, FONTS["sm"], C["text2"],
                      self._col_centers[i], self._piece_header_y + 2, "midtop")
            hint_lines = wrap_text(T(hint_key), FONTS["xs"], self._spinner_w + 24)
            for j, line in enumerate(hint_lines[:3]):
                draw_text(content, line, FONTS["xs"], C["text3"],
                          self._col_centers[i], self._piece_header_y + 22 + j * 13, "midtop")

        row_h = 52   # must match _layout
        for i, t in enumerate(PIECE_TYPES):
            # spinner is already positioned; just draw it and the label centred on same row
            sp0 = self.spinners_piece[("move", t)]
            label_cy = sp0.rect.centery
            draw_text(content, TP(t), FONTS["med"], C["text"],
                      self._x_label, label_cy, "midleft")
            for kind in ["move","res_cost","res_count"]:
                self.spinners_piece[(kind, t)].draw(content)

        pygame.draw.line(content, C["border"],
                         (self._x_start, self._sep_y),
                         (self._x_start + self._max_w, self._sep_y), 1)

        draw_text(content, T("global_settings"), FONTS["med"], C["text2"],
                  self._x_start + 10, self._global_header_y - 8, "topleft")

        labels_hints = [
            (T("max_actions"), "hint_max_actions"),
            (T("crit_bonus"),  "hint_crit"),
            (T("fail_penalty"), "hint_fail"),
            (T("castle_cost_lbl"), "hint_castle"),
        ]
        keys = ["max_actions","crit_ap","fail_penalty","castle_cost"]
        for k, (lbl, hint_key) in zip(keys, labels_hints):
            sp = self.spinners_global[k]
            row_top = sp.rect.top - 29
            # Available width for label/hint = space before spinner
            avail_w = sp.rect.left - self._x_global_label - 12
            draw_text(content, lbl, FONTS["med"], C["text"],
                      self._x_global_label, row_top + 2, "topleft")
            hint_lines = wrap_text(T(hint_key), FONTS["xs"], avail_w)
            for j, line in enumerate(hint_lines[:2]):
                draw_text(content, line, FONTS["xs"], C["text3"],
                          self._x_global_label, row_top + 20 + j * 13, "topleft")
            sp.draw(content)

        # En passant toggle
        ep_lbl_col = C["text3"] if self.locked else C["text"]
        ep_sp = self.ep_toggle
        avail_w_ep = ep_sp.rect.left - self._x_global_label - 12
        draw_text(content, T("allow_ep"), FONTS["med"], ep_lbl_col,
                  self._x_global_label, self._ep_y + 2, "topleft")
        hint_ep_lines = wrap_text(T("hint_ep"), FONTS["xs"], avail_w_ep)
        for j, line in enumerate(hint_ep_lines[:2]):
            draw_text(content, line, FONTS["xs"], C["text3"],
                      self._x_global_label, self._ep_y + 20 + j * 13, "topleft")
        self.ep_toggle.disabled = self.locked
        self.ep_toggle.draw(content)

        # Save/Reset — disable when locked
        self.btn_save.disabled = self.locked
        self.btn_reset.disabled = self.locked
        self.btn_save.draw(content)
        self.btn_reset.draw(content)

        # Flash animation over the triggered button
        if self._flash:
            which, t0 = self._flash
            elapsed = _time.monotonic() - t0
            FLASH_DUR = 3.0
            if elapsed < FLASH_DUR:
                prog = elapsed / FLASH_DUR
                # Alpha: spike up then fade
                alpha = int(220 * (1 - prog) ** 1.5)
                btn = self.btn_save if which == "save" else self.btn_reset
                # Draw coloured overlay
                flash_col = (60, 200, 100) if which == "save" else (200, 100, 60)
                fl = pygame.Surface((btn.rect.width, btn.rect.height), pygame.SRCALPHA)
                fl.fill((*flash_col, alpha))
                pygame.draw.rect(fl, (*flash_col, min(255, alpha + 60)),
                                 (0, 0, btn.rect.width, btn.rect.height), 2, border_radius=8)
                content.blit(fl, btn.rect.topleft)
                # Checkmark / X text
                icon = "✓  Сохранено" if (which == "save" and LANG == "ru") else \
                       "✓  Saved"    if which == "save" else \
                       "↺  Сброшено" if LANG == "ru" else "↺  Reset"
                icon_alpha = min(255, int(255 * (1 - prog * 0.5)))
                icon_col = (220, 255, 220, icon_alpha) if which == "save" else (255, 220, 200, icon_alpha)
                ic = FONTS["sm"].render(icon, True, icon_col[:3])
                ic.set_alpha(icon_alpha)
                content.blit(ic, ic.get_rect(center=btn.rect.center))
            else:
                self._flash = None


        surf.fill(C["bg"])
        surf.blit(content, (0, -self.scroll_y))

        # Full-screen lock overlay (drawn on top)
        if self.locked:
            overlay = pygame.Surface((surf.get_width(), surf.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            surf.blit(overlay, (0, 0))

            cx = surf.get_width() // 2
            cy = surf.get_height() // 2 - 30

            # Draw lock icon using shapes (no emoji needed)
            lk_w, lk_h = 52, 44
            lk_x, lk_y = cx - lk_w // 2, cy - lk_h // 2 - 10
            # Shackle (arc = two lines + top rect)
            shackle_col = (200, 170, 60)
            pygame.draw.rect(surf, shackle_col,
                             (lk_x + 10, lk_y - 22, lk_w - 20, 26), 0, border_radius=10)
            pygame.draw.rect(surf, (0, 0, 0, 0),
                             (lk_x + 16, lk_y - 16, lk_w - 32, 20), 0)
            pygame.draw.rect(surf, (18, 18, 24),
                             (lk_x + 16, lk_y - 16, lk_w - 32, 20))
            # Body
            pygame.draw.rect(surf, shackle_col,
                             (lk_x, lk_y, lk_w, lk_h), 0, border_radius=8)
            # Keyhole
            kh_c = (40, 30, 10)
            pygame.draw.circle(surf, kh_c, (cx, lk_y + 18), 8)
            pygame.draw.rect(surf, kh_c, (cx - 4, lk_y + 18, 8, 14))

            # Text
            line1 = T("settings_locked")
            line2 = T("settings_lock_hint")
            draw_text(surf, line1, FONTS["big"], (230, 195, 80),
                      cx, lk_y + lk_h + 20, "midtop")
            draw_text(surf, line2, FONTS["sm"], (160, 135, 60),
                      cx, lk_y + lk_h + 52, "midtop")

        # Scrollbar (only when not locked)
        if self.content_h > surf.get_height() and not self.locked:
            sb_w = 6
            sb_x = surf.get_width() - sb_w - 4
            sb_h = surf.get_height()
            ratio = surf.get_height() / self.content_h
            thumb_h = max(30, int(sb_h * ratio))
            thumb_y = int((self.scroll_y / max_scroll) * (sb_h - thumb_h)) if max_scroll > 0 else 0
            pygame.draw.rect(surf, C["bg3"], (sb_x, 0, sb_w, sb_h), border_radius=3)
            pygame.draw.rect(surf, C["border2"], (sb_x, thumb_y, sb_w, thumb_h), border_radius=3)



    def handle(self, event):
        def offset_event(e):
            if e.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                ne = pygame.event.Event(e.type, dict(e.__dict__))
                if hasattr(ne, "pos"):
                    ne.pos = (ne.pos[0], ne.pos[1] + self.scroll_y)
                return ne
            return e

        if event.type == pygame.MOUSEWHEEL:
            self.scroll_y -= event.y * 30
            return None

        if self.locked:
            return None   # all interactions blocked during game

        ev = offset_event(event)
        for sp in list(self.spinners_piece.values()) + list(self.spinners_global.values()):
            sp.handle(ev)
        self.ep_toggle.handle(ev)

        for btn in [self.btn_save, self.btn_reset]:
            if event.type == pygame.MOUSEMOTION:
                btn.update_hover((event.pos[0], event.pos[1] + self.scroll_y))

        if self.btn_save.clicked(ev):
            self._apply()
            self._flash = ("save", _time.monotonic())
            return "saved"
        if self.btn_reset.clicked(ev):
            self._reset()
            self._flash = ("reset", _time.monotonic())
            return "reset"
        return None

    def _apply(self):
        for t in PIECE_TYPES:
            settings["move_cost"][t] = self.spinners_piece[("move", t)].value
            settings["res_cost"][t] = self.spinners_piece[("res_cost", t)].value
            settings["res_count"][t] = self.spinners_piece[("res_count", t)].value
        for k in ["max_actions","crit_ap","fail_penalty","castle_cost"]:
            settings[k] = self.spinners_global[k].value
        settings["allow_ep"] = self.ep_toggle.value

    def _reset(self):
        global settings
        settings = copy.deepcopy(DEFAULT_SETTINGS)
        self._build_widgets()

    def refresh_labels(self):
        self.btn_save.label = T("save_settings")
        self.btn_reset.label = T("reset_settings")


def get_tutorial_steps():
    if LANG == "ru":
        return [
            ("Добро пожаловать!",
             "Шахматы Зла — это шахматы с элементом удачи. В начале каждого хода вы бросаете 2 кубика (2к6) "
             "и получаете Очки Действий (ОД), которые тратите на перемещение фигур."),
            ("Цены фигур",
             "Каждый ход фигуры стоит ОД:\n\n"
             "Король — 8 ОД\nФерзь — 6 ОД\nЛадья — 5 ОД\nСлон — 3 ОД\nКонь — 3 ОД\nПешка — 1 ОД\n\n"
             "Рокировка стоит 5 ОД (цена ладьи)."),
            ("Ограничения хода",
             "За один ход вы можете:\n\n"
             "• Сделать не более 3 действий\n• Двигать каждую фигуру только 1 раз\n• Тратить ОД пока они не кончатся\n\n"
             "Если ОД меньше, чем стоит фигура — она недоступна для хода."),
            ("Критические броски",
             "Бросок 12 (максимум) — Критическая удача!\nОдна выбранная фигура может сходить дважды за ход.\n\n"
             "Бросок 2 (минимум) — Критическая неудача!\nВы теряете 1 ОД."),
            ("Шах и ход короля",
             "Когда ваш король под шахом — клетка подсвечивается красным.\n\n"
             "Ход короля под шахом стоит ВСЕ ваши ОД, независимо от их количества.\n\n"
             "Если у вас мало ОД, это может быть проблемой!"),
            ("Королевский Гамбит",
             "Если у вас остался только Король — активируется Королевский Гамбит.\n\n"
             "В этом режиме ход короля стоит всего 1 ОД (но не более 3 ходов за раз).\n\n"
             "Ваш одинокий король становится мобильнее!"),
            ("Столкновение Судеб",
             "Если у обоих игроков остались только Короли — начинается Столкновение Судеб!\n\n"
             "Теперь можно тратить ОД на воскрешение мёртвых фигур.\n\n"
             "Пешки воскресить нельзя. Ферзь воскрешается лишь раз."),
            ("Завершение игры",
             "Игра заканчивается:\n\n"
             "• Матом — король противника не может спастись\n"
             "• Патом — у противника нет ходов, но шаха нет (ничья)\n\n"
             "Удачи в игре!"),
        ]
    else:
        return [
            ("Welcome!",
             "Chess of Evil is chess with a luck element. At the start of each turn you roll 2d6 "
             "and receive Action Points (AP) which you spend on moving pieces."),
            ("Piece Costs",
             "Each piece move costs AP:\n\nKing — 8 AP\nQueen — 6 AP\nRook — 5 AP\nBishop — 3 AP\nKnight — 3 AP\nPawn — 1 AP\n\n"
             "Castling costs 5 AP (rook price)."),
            ("Turn Limits",
             "Each turn you may:\n\n• Take at most 3 actions\n• Move each piece only once\n• Spend AP until they run out\n\n"
             "If AP < piece cost — that piece is unavailable."),
            ("Critical Rolls",
             "Roll 12 (max) — Critical Hit!\nOne chosen piece may move twice this turn.\n\n"
             "Roll 2 (min) — Critical Fail!\nYou lose 1 AP."),
            ("Check & King Move",
             "When your king is in check — the square is highlighted red.\n\n"
             "Moving the king while in check costs ALL your AP.\n\n"
             "Few AP when in check can be very dangerous!"),
            ("Royal Gambit",
             "If only your King remains — Royal Gambit activates!\n\n"
             "King's move costs just 1 AP (still up to 3 actions per turn).\n\n"
             "Your lone king becomes more mobile!"),
            ("Clash of Fates",
             "If BOTH players have only Kings — Clash of Fates begins!\n\n"
             "You can now spend AP to resurrect dead pieces.\n\n"
             "Pawns cannot be resurrected. Queens only once."),
            ("End of Game",
             "The game ends by:\n\n• Checkmate — opponent's king cannot escape\n"
             "• Stalemate — opponent has no moves but isn't in check (draw)\n\nGood luck!"),
        ]


class TutorialScreen:
    def __init__(self):
        self.step = 0
        self.btn_next = Button((0,0,160,40), T("learn_next"),
                                color=C["accent2"], hover_color=C["accent"])
        self.btn_prev = Button((0,0,160,40), T("learn_prev"))
        self.btn_exit = Button((0,0,140,40), T("learn_exit"))

    # ── Mini board illustration helpers ──────────────────────
    def _draw_mini_board(self, surf, x, y, size, pieces, highlights=None, arrows=None):
        """Draw a small chess diagram. pieces = {(r,c): piece_char}"""
        sq = size // 8
        bsize = sq * 8
        for r in range(8):
            for c in range(8):
                light = (r + c) % 2 == 0
                rect = pygame.Rect(x + c * sq, y + r * sq, sq, sq)
                col = (240, 217, 181) if light else (181, 136, 99)
                pygame.draw.rect(surf, col, rect)
                if highlights and (r, c) in highlights:
                    rgba = highlights[(r, c)]
                    hl = pygame.Surface((sq, sq), pygame.SRCALPHA)
                    if len(rgba) == 4:
                        hl.fill(rgba)
                    else:
                        hl.fill((*rgba, 140))
                    surf.blit(hl, rect.topleft)
        # Border
        pygame.draw.rect(surf, (80, 55, 30), (x - 2, y - 2, bsize + 4, bsize + 4), 2, border_radius=3)
        # Pieces
        for (r, c), p in pieces.items():
            rect = pygame.Rect(x + c * sq, y + r * sq, sq, sq)
            psize = int(sq * 0.72)
            ps = piece_surface(p, psize)
            surf.blit(ps, ps.get_rect(center=rect.center))
        # Arrows
        if arrows:
            for (r1,c1), (r2,c2) in arrows:
                ax1 = x + c1 * sq + sq // 2
                ay1 = y + r1 * sq + sq // 2
                ax2 = x + c2 * sq + sq // 2
                ay2 = y + r2 * sq + sq // 2
                pygame.draw.line(surf, (255, 200, 0), (ax1, ay1), (ax2, ay2), 3)
                # Arrowhead
                dx, dy = ax2 - ax1, ay2 - ay1
                length = max(1, (dx**2 + dy**2) ** 0.5)
                ux, uy = dx / length, dy / length
                px, py = -uy, ux
                tip = (ax2, ay2)
                left = (int(ax2 - ux*10 + px*5), int(ay2 - uy*10 + py*5))
                right = (int(ax2 - ux*10 - px*5), int(ay2 - uy*10 - py*5))
                pygame.draw.polygon(surf, (255, 200, 0), [tip, left, right])

    def _draw_dice_example(self, surf, x, y, d1, d2, label, player_color=None):
        """Draw two dice with a label below."""
        die_sz = 44; gap = 10
        r1 = pygame.Rect(x, y, die_sz, die_sz)
        r2 = pygame.Rect(x + die_sz + gap, y, die_sz, die_sz)
        draw_die(surf, d1, r1, player_color=player_color)
        draw_die(surf, d2, r2, player_color=player_color)
        draw_text(surf, label, FONTS["xs"], C["text2"],
                  x + die_sz + gap // 2, y + die_sz + 6, "midtop")

    def _get_illustration(self, step_idx, area):
        """Return a Surface with the illustration for this step."""
        w, h = area.width, area.height
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))
        cx, cy = w // 2, h // 2

        mini_sz = min(w - 20, h - 20, 240)
        mini_sz = (mini_sz // 8) * 8
        mx = cx - mini_sz // 2
        my = cy - mini_sz // 2

        if step_idx == 0:  # Welcome - full starting position overview
            pieces = {}
            for c, p in enumerate("RNBQKBNR"):
                pieces[(0, c)] = p.lower(); pieces[(7, c)] = p
            for c in range(8):
                pieces[(1, c)] = "p"; pieces[(6, c)] = "P"
            self._draw_mini_board(surf, mx, my, mini_sz, pieces)

        elif step_idx == 1:  # Piece costs - show piece values
            sq = mini_sz // 8
            pieces_row = [("K","8"),("Q","6"),("R","5"),("B","3"),("N","3"),("P","1")]
            col_w = min(w // 6, 70)
            start_x = cx - len(pieces_row) * col_w // 2
            for i, (pt, cost) in enumerate(pieces_row):
                px2 = start_x + i * col_w + col_w // 2
                py2 = cy - 20
                ps = piece_surface(pt, 36)
                surf.blit(ps, ps.get_rect(center=(px2, py2)))
                draw_text(surf, cost + " ОД" if LANG == "ru" else cost + " AP",
                          FONTS["xs"], C["gold2"], px2, py2 + 26, "midtop")

        elif step_idx == 2:  # Turn limits - show board with arrows
            pieces = {(6,4):"P", (4,4):"P"}
            hl = {(5,4):(90,180,90,140), (4,4):(90,130,220,160)}
            self._draw_mini_board(surf, mx, my, mini_sz, pieces, hl,
                                  [((6,4),(4,4))])

        elif step_idx == 3:  # Critical rolls
            self._draw_dice_example(surf, cx - 55, cy - 40, 6, 6, "= 12 ★ КРИТ" if LANG=="ru" else "= 12 ★ CRIT", "W")
            self._draw_dice_example(surf, cx - 55, cy + 30, 1, 1, "= 2  ✗ ПРОВАЛ" if LANG=="ru" else "= 2  ✗ FAIL", "B")

        elif step_idx == 4:  # Check
            pieces = {(3,4):"K", (0,4):"q", (4,3):"r"}
            hl = {(3,4):(220,60,60,180)}
            self._draw_mini_board(surf, mx, my, mini_sz, pieces, hl)

        elif step_idx == 5:  # Royal Gambit
            pieces = {(4,4):"K"}
            hl = {(3,3):(90,180,90,140),(3,4):(90,180,90,140),(3,5):(90,180,90,140),
                  (4,3):(90,180,90,140),(4,5):(90,180,90,140),
                  (5,3):(90,180,90,140),(5,4):(90,180,90,140),(5,5):(90,180,90,140)}
            self._draw_mini_board(surf, mx, my, mini_sz, pieces, hl)
            draw_text(surf, "1 ОД" if LANG=="ru" else "1 AP",
                      FONTS["sm"], C["gold2"], cx, my + mini_sz + 8, "midtop")

        elif step_idx == 6:  # Clash of Fates
            pieces = {(3,3):"K", (5,5):"k"}
            self._draw_mini_board(surf, mx, my, mini_sz, pieces)
            # Show resurrectable pieces
            res_pieces = ["Q","R","B","N"]
            icon_w = min(w // 5, 50)
            iy = my + mini_sz + 14
            for i, pt in enumerate(res_pieces):
                ipx = cx - len(res_pieces)*icon_w//2 + i*icon_w + icon_w//2
                ps = piece_surface(pt, 28)
                surf.blit(ps, ps.get_rect(center=(ipx, iy + 14)))
                draw_text(surf, "+", FONTS["sm"], C["accent"], ipx, iy - 2, "midtop")

        elif step_idx == 7:  # Castling / En passant
            sq2 = mini_sz // 8
            # Castling side (left)
            p_c = {(7,4):"K",(7,7):"R"}
            hl_c = {(7,6):(210,175,50,160),(7,5):(210,175,50,100)}
            self._draw_mini_board(surf, mx - mini_sz//2 - 10, my, mini_sz, p_c, hl_c)
            draw_text(surf, "0-0", FONTS["sm"], C["gold2"],
                      mx - mini_sz//2 - 10 + mini_sz//2, my + mini_sz + 6, "midtop")
            # EP side (right)
            p_ep = {(3,4):"p",(3,3):"P"}
            hl_ep = {(2,3):(60,200,220,160)}
            self._draw_mini_board(surf, mx + mini_sz//2 + 10, my, mini_sz, p_ep, hl_ep,
                                  [((3,3),(2,3))])
            draw_text(surf, "e.p.", FONTS["sm"], C["accent"],
                      mx + mini_sz//2 + 10 + mini_sz//2, my + mini_sz + 6, "midtop")

        else:  # End of game
            pieces = {(0,4):"k", (2,3):"Q", (1,2):"R"}
            self._draw_mini_board(surf, mx, my, mini_sz, pieces,
                                  {(0,4):(220,60,60,200)})
            draw_text(surf, "MAT" if LANG=="en" else "МАТ",
                      FONTS["big"], C["red2"], cx, my + mini_sz + 8, "midtop")

        return surf

    def draw(self, surf):
        sw, sh = surf.get_width(), surf.get_height()
        surf.fill(C["bg"])

        # Gradient background
        for yy in range(0, sh, 4):
            t = yy / sh
            col = (int(18+t*5), int(18+t*3), int(24+t*9))
            pygame.draw.line(surf, col, (0, yy), (sw, yy))

        steps = get_tutorial_steps()
        total = len(steps)
        self.step = max(0, min(self.step, total - 1))
        title, body = steps[self.step]

        # ── Progress bar ──────────────────────────────────────
        margin = 40
        bar_h = 6
        bar_y = 16
        counter_str = f"{self.step + 1} / {total}"
        counter_w = FONTS["sm"].size(counter_str)[0] + 16
        bar_x = margin
        bar_w = sw - margin * 2 - counter_w - 8

        pygame.draw.rect(surf, C["bg3"], (bar_x, bar_y, bar_w, bar_h), border_radius=3)
        fill_w = int(bar_w * (self.step + 1) / total)
        pygame.draw.rect(surf, C["accent"], (bar_x, bar_y, fill_w, bar_h), border_radius=3)

        seg = bar_w / total
        for i in range(total):
            dx = int(bar_x + seg * i + seg / 2)
            dy = bar_y + bar_h // 2
            col = C["accent"] if i <= self.step else C["bg3"]
            if i == self.step:
                pygame.draw.circle(surf, C["text"], (dx, dy), 7)
            pygame.draw.circle(surf, col, (dx, dy), 5)

        draw_text(surf, counter_str, FONTS["sm"], C["text2"],
                  bar_x + bar_w + 10, bar_y + bar_h // 2, "midleft")

        # ── Content area ──────────────────────────────────────
        gap_between = 18
        content_y = bar_y + bar_h + 18
        content_h = sh - content_y - 68
        left_w = int(sw * 0.46)
        right_w = sw - margin * 2 - left_w - gap_between

        card_pad = 16
        left_x = margin
        draw_rect(surf, C["panel"], (left_x, content_y, left_w, content_h), 10, 1, C["border"])

        draw_text(surf, title, FONTS["big"], C["gold2"],
                  left_x + card_pad, content_y + 14)
        title_h = FONTS["big"].get_height()
        sep_y = content_y + 14 + title_h + 8
        pygame.draw.line(surf, C["border"],
                         (left_x + card_pad, sep_y),
                         (left_x + left_w - card_pad, sep_y), 1)

        text_x = left_x + card_pad
        text_y = sep_y + 10
        max_tw = left_w - card_pad * 2
        lines = wrap_text(body, FONTS["med"], max_tw)
        lh = FONTS["med"].get_height() + 5
        for i, line in enumerate(lines):
            ly = text_y + i * lh
            if ly + lh > content_y + content_h - 8: break
            draw_text(surf, line, FONTS["med"], C["text"], text_x, ly)

        illus_x = left_x + left_w + gap_between
        illus_area = pygame.Rect(illus_x, content_y, right_w, content_h)
        draw_rect(surf, C["panel2"], illus_area, 10, 1, C["border2"])
        illus_surf = self._get_illustration(self.step, illus_area)
        surf.blit(illus_surf, illus_area.topleft)
        # Navigation buttons
        btn_y = sh - 56
        bw = 160; gap = 16; cx2 = sw // 2
        self.btn_prev.rect = pygame.Rect(cx2 - bw - gap // 2, btn_y, bw, 40)
        self.btn_next.rect = pygame.Rect(cx2 + gap // 2, btn_y, bw, 40)
        self.btn_exit.rect = pygame.Rect(sw - 160, btn_y, 140, 40)

        self.btn_prev.disabled = self.step == 0
        self.btn_next.label = T("learn_next") if self.step < total - 1 else T("learn_exit")
        self.btn_prev.draw(surf)
        self.btn_next.draw(surf)
        self.btn_exit.draw(surf)

    def handle(self, event):
        steps = get_tutorial_steps()
        for btn in [self.btn_next, self.btn_prev, self.btn_exit]:
            if event.type == pygame.MOUSEMOTION:
                btn.update_hover(event.pos)
        if self.btn_next.clicked(event):
            if self.step < len(steps) - 1: self.step += 1
            else: return "exit"
        if self.btn_prev.clicked(event):
            if self.step > 0: self.step -= 1
        if self.btn_exit.clicked(event):
            return "exit"
        return None

    def refresh_labels(self):
        self.btn_next.label = T("learn_next")
        self.btn_prev.label = T("learn_prev")
        self.btn_exit.label = T("learn_exit")
class GameScreen:
    def __init__(self):
        self.gs = GameState()
        self.gs.add_log(T("log_newgame"), "sys")
        self.btn_roll = Button((0,0,100,38), T("roll_dice"),
                                color=C["accent2"], hover_color=C["accent"])
        self.btn_end  = Button((0,0,100,38), T("end_turn"))
        self.btn_new  = Button((0,0,100,36), T("new_game"))
        self.dice_vals = (0, 0)
        self.res_buttons = []
        self.promo_buttons = []
        self._gameover_btn = None
        self.bx = self.by = 0
        self.bsize = 8; self.sq = 1
        self.sx = self.sy = self.sw_panel = 0
        # Animation state
        self.anim: PieceAnim | None = None
        self._last_move = None
        self._frame_time = 0.0
        # Bot settings
        self.bot_enabled = False
        self.bot_color = "B"      # bot plays as black by default
        self.bot_difficulty = "medium"
        self._bot_pending = False  # waiting to fire bot move
        self._bot_delay = 0.0      # time when bot was scheduled
        # LAN session
        self.lan: LanSession | None = None
        self._request_mode_screen = False

    def new_game(self):
        self.gs = GameState()
        self.gs.add_log(T("log_newgame"), "sys")
        self.dice_vals = (0, 0)
        self.anim = None
        self._last_move = None
        self._bot_pending = False

    def _layout(self, w, h):
        side_w = 296
        frame = 18         # board decorative frame thickness
        margin_top = 22
        margin_bot = 28    # extra bottom breathing room
        margin_left = 22
        board_gap = 22     # gap between board right edge and side panel

        avail_w = w - side_w - margin_left * 2 - board_gap - frame * 2
        avail_h = h - margin_top - margin_bot - frame * 2
        self.bsize = min(avail_w, avail_h)
        self.bsize = (self.bsize // 8) * 8
        if self.bsize < 240: self.bsize = 240
        self.sq = self.bsize // 8
        # Board position leaves room for frame on all sides
        self.bx = margin_left + frame + (avail_w - self.bsize) // 2
        self.by = margin_top + frame + (avail_h - self.bsize) // 2

        self.sx = self.bx + self.bsize + frame + board_gap
        self.sy = margin_top
        self.sw_panel = w - self.sx - margin_left

        bx2 = self.sx + 10
        bw = self.sw_panel - 20
        panel_end = self.sy + 54 + 4 + 54
        btn_y = panel_end + 24
        self.btn_roll.rect = pygame.Rect(bx2, btn_y, bw, 38)
        self.btn_end.rect  = pygame.Rect(bx2, btn_y + 44, bw, 38)
        self.btn_new.rect  = pygame.Rect(bx2, h - margin_bot - 40, bw, 38)

    def click_to_rc(self, mx, my):
        if not (self.bx <= mx < self.bx + self.bsize and self.by <= my < self.by + self.bsize):
            return None
        c = (mx - self.bx) // self.sq
        r = (my - self.by) // self.sq
        if 0 <= r < 8 and 0 <= c < 8:
            return (int(r), int(c))
        return None

    def draw(self, surf):
        self._layout(surf.get_width(), surf.get_height())
        surf.fill(C["bg"])
        # Gradient background
        for y in range(0, surf.get_height(), 4):
            t = y / surf.get_height()
            col = (
                int(18 + t * 6),
                int(18 + t * 4),
                int(24 + t * 8)
            )
            pygame.draw.line(surf, col, (0, y), (surf.get_width(), y))
        self._draw_board(surf)
        self._draw_sidebar(surf)
        if self.gs.promo_at:
            self._draw_promo(surf)
        elif self.gs.over:
            self._draw_status_overlay(surf)

    def _draw_board(self, surf):
        gs = self.gs
        sq = self.sq; bx = self.bx; by = self.by

        # ── Decorative frame ─────────────────────────────────
        draw_board_frame(surf, bx, by, self.bsize, sq)

        # Pulse alpha for selection glow
        pulse = _ease_pulse(1.4)

        # ── Squares ──────────────────────────────────────────
        for r in range(8):
            for c in range(8):
                light = (r + c) % 2 == 0
                rect = pygame.Rect(bx + c * sq, by + r * sq, sq, sq)
                base = C["sq_light"] if light else C["sq_dark"]
                pygame.draw.rect(surf, base, rect)

                # Last-move trail
                if self._last_move:
                    fr, fc, tr, tc = self._last_move
                    if (r, c) in ((fr, fc), (tr, tc)):
                        trail = pygame.Surface((sq, sq), pygame.SRCALPHA)
                        trail.fill((255, 215, 0, 55))
                        surf.blit(trail, rect.topleft)

                # Check highlight
                if gs.check_sq and (r, c) == gs.check_sq:
                    hl = pygame.Surface((sq, sq), pygame.SRCALPHA)
                    a = int(140 + 80 * pulse)
                    hl.fill((220, 40, 40, a))
                    surf.blit(hl, rect.topleft)

                # Selection highlight (pulsing)
                elif gs.sel and (r, c) == gs.sel:
                    hl = pygame.Surface((sq, sq), pygame.SRCALPHA)
                    a = int(120 + 80 * pulse)
                    hl.fill((80, 130, 220, a))
                    surf.blit(hl, rect.topleft)

                # Legal move dots / capture highlights
                elif gs.legal and any(lr == r and lc == c for lr, lc, _ in gs.legal):
                    # Find the specific move to check its special type
                    move_sp = next((sp for lr, lc, sp in gs.legal if lr == r and lc == c), None)
                    is_cap = bool(gs.board[r][c])
                    is_castle = move_sp in ("ck", "cq")
                    is_ep = move_sp == "ep"

                    hl = pygame.Surface((sq, sq), pygame.SRCALPHA)

                    if is_cap and not is_ep:
                        # Red ring for captures
                        col = (210, 60, 60, 160)
                        pygame.draw.rect(hl, col, (0, 0, sq, sq))
                        inner = pygame.Surface((sq-12, sq-12), pygame.SRCALPHA)
                        inner.fill((*base, 0))
                        hl.blit(inner, (6, 6))
                        surf.blit(hl, rect.topleft)
                    elif is_castle:
                        # Gold diamond shape for castling
                        cx2, cy2 = sq // 2, sq // 2
                        d = max(8, sq // 4)
                        points = [(cx2, cy2-d), (cx2+d, cy2), (cx2, cy2+d), (cx2-d, cy2)]
                        pygame.draw.polygon(hl, (210, 175, 50, 180), points)
                        pygame.draw.polygon(hl, (255, 220, 80, 220), points, 2)
                        surf.blit(hl, rect.topleft)
                        # Small crown text hint
                        draw_text(surf, "♜↔♚" if False else "0-0", FONTS["coord"],
                                  (220, 190, 70), rect.centerx, rect.bottom - 10, "center")
                    elif is_ep:
                        # Cyan ghost dot for en passant
                        dot_r = max(6, sq // 6)
                        pygame.draw.circle(hl, (60, 200, 220, 160),
                                           (sq // 2, sq // 2), dot_r)
                        # Ghost pawn outline
                        ghost_sz = max(8, sq // 4)
                        pygame.draw.circle(hl, (60, 220, 240, 80),
                                           (sq // 2, sq // 2), ghost_sz)
                        pygame.draw.circle(hl, (60, 220, 240, 140),
                                           (sq // 2, sq // 2), ghost_sz, 2)
                        surf.blit(hl, rect.topleft)
                        draw_text(surf, "ep", FONTS["coord"],
                                  (80, 220, 240), rect.centerx, rect.bottom - 10, "center")
                    else:
                        # Standard green dot for normal moves
                        dot_r = max(6, sq // 6)
                        pygame.draw.circle(hl, (60, 160, 80, 140),
                                           (sq // 2, sq // 2), dot_r)
                        surf.blit(hl, rect.topleft)

        # ── Pieces (skip animating piece's source square) ────
        anim_done = self.anim is None or self.anim.is_done()
        if anim_done:
            self.anim = None

        for r in range(8):
            for c in range(8):
                p = gs.board[r][c]
                if not p: continue
                # If this piece is being animated, skip it here
                if (self.anim and not self.anim.is_done()
                        and self.anim.piece == p
                        and self._last_move
                        and (r, c) == (self._last_move[2], self._last_move[3])):
                    continue

                rect = pygame.Rect(bx + c * sq, by + r * sq, sq, sq)
                psize = int(sq * 0.74)
                cx, cy = rect.centerx, rect.centery

                # Piece centred on square (no shadow - kept breaking)
                surf_p = piece_surface(p, psize)
                surf.blit(surf_p, surf_p.get_rect(center=(cx, cy)))

        # ── Animated sliding piece (drawn on top) ────────────
        if self.anim and not self.anim.is_done():
            ax, ay = self.anim.pos()
            psize = int(sq * 0.74)
            surf_p = piece_surface(self.anim.piece, psize)
            surf.blit(surf_p, surf_p.get_rect(center=(int(ax), int(ay) - 3)))
    def _draw_sidebar(self, surf):
        gs = self.gs
        sx = self.sx; sy = self.sy; sw = self.sw_panel
        bx2 = sx + 10; bw = sw - 20

        # ── Player panels ────────────────────────────────────
        panel_h = 54
        for i, color in enumerate(["W", "B"]):
            py = sy + i * (panel_h + 4)
            is_active = gs.turn == color and not gs.over
            bg = C["panel2"] if is_active else C["panel"]
            border = C["accent"] if is_active else C["border"]
            draw_rect(surf, bg, (sx, py, sw, panel_h), 8, 2, border)
            name = T("white") if color == "W" else T("black")
            psurf = piece_surface("K" if color == "W" else "k", 22)
            surf.blit(psurf, (bx2 - 4, py + 6))
            draw_text(surf, name, FONTS["med"],
                      C["text"] if is_active else C["text2"],
                      bx2 + 30, py + 8)
            od_val = gs.od[color]
            draw_text(surf, f"{od_val} {T('ap_label')}", FONTS["big"],
                      C["gold2"] if is_active else C["text2"],
                      sx + sw - 10, py + 8, "topright")
            draw_rect(surf, C["bg3"], (bx2, py + 42, bw, 6), 3)
            fill_w = int(bw * min(1.0, od_val / 12))
            fill_c = C["red2"] if od_val <= 2 and gs.rolled else C["accent"]
            if fill_w > 0:
                draw_rect(surf, fill_c, (bx2, py + 42, fill_w, 6), 3)

        panel_end = sy + 2 * panel_h + 4
        badge_y = panel_end + 8

        # ── Phase badge (only gambit/clash) ──────────────────
        if gs.phase != "normal":
            phase_lbl = T("phase_gambit") if gs.phase == "gambit" else T("phase_clash")
            badge_col = C["gold2"] if gs.phase == "gambit" else C["accent"]
            badge_bg  = (40, 35, 10) if gs.phase == "gambit" else (15, 25, 50)
            lw = FONTS["sm"].size(phase_lbl)[0] + 20
            draw_rect(surf, badge_bg, (sx + (sw - lw) // 2, badge_y, lw, 22), 11)
            draw_text(surf, phase_lbl, FONTS["sm"], badge_col,
                      sx + sw // 2, badge_y + 11, "center")
            badge_h = 28
        else:
            badge_h = 0

        # ── Buttons ───────────────────────────────────────────
        btn_y = badge_y + badge_h + 4
        self.btn_roll.rect.x = bx2; self.btn_roll.rect.y = btn_y; self.btn_roll.rect.w = bw
        self.btn_end.rect.x  = bx2; self.btn_end.rect.y  = btn_y + 44; self.btn_end.rect.w = bw
        self.btn_roll.disabled = gs.rolled or gs.over
        self.btn_end.disabled  = not gs.rolled or gs.over
        self.btn_roll.draw(surf)
        self.btn_end.draw(surf)

        # ── Dice ──────────────────────────────────────────────
        die_size = 44; gap = 14
        dy = self.btn_end.rect.bottom + 14
        total_dw = 2 * die_size + gap
        dx = sx + (sw - total_dw) // 2
        d1, d2 = self.dice_vals
        crit = d1 + d2 == 12 and d1 > 0
        fail = d1 + d2 == 2 and d1 > 0
        pc_ = gs.turn if gs.rolled else None
        draw_die(surf, d1, pygame.Rect(dx, dy, die_size, die_size), crit, fail, pc_)
        draw_die(surf, d2, pygame.Rect(dx + die_size + gap, dy, die_size, die_size), crit, fail, pc_)

        # ── Status line ───────────────────────────────────────
        acts_y = dy + die_size + 8
        if gs.rolled:
            acts_str = T("actions_label", gs.act_used, settings["max_actions"])
            if gs.crit and not gs.crit_used:
                acts_str += ("  ★ КРИТ" if LANG == "ru" else "  ★ CRIT")
            acts_col = C["gold2"] if gs.crit and not gs.crit_used else C["text2"]
        else:
            acts_str = T("roll_prompt"); acts_col = C["text3"]
        draw_text(surf, acts_str, FONTS["sm"], acts_col, sx + sw // 2, acts_y, "midtop")

        msg_y = acts_y + 22
        if not gs.over and gs.check_sq:
            en_name = T("white") if opp(gs.turn) == "W" else T("black")
            draw_text(surf, f"{T('check')} ({en_name})", FONTS["sm"],
                      C["red2"], sx + sw // 2, msg_y, "midtop")
            msg_y += 22

        # ── Resurrect ─────────────────────────────────────────
        self.res_buttons = []
        if gs.phase == "clash" and gs.rolled and not gs.over:
            res_items = gs.get_resurrectable()
            if res_items:
                draw_text(surf, T("resurrect"), FONTS["xs"], C["text3"], bx2, msg_y)
                msg_y += 18
                for t, cost in res_items:
                    label = f"{TP(t)}  {cost} {T('ap_label')}"
                    btn = Button((bx2, msg_y, bw, 28), label,
                                  color=C["bg3"], hover_color=C["panel2"], font=FONTS["sm"])
                    btn.disabled = (gs.act_used >= settings["max_actions"] or gs.od[gs.turn] < cost)
                    btn.draw(surf)
                    self.res_buttons.append((btn, t))
                    msg_y += 32

        # ── Log ───────────────────────────────────────────────
        log_bottom = self.btn_new.rect.top - 8
        log_top = max(msg_y + 8, log_bottom - 170)
        log_h = log_bottom - log_top
        if log_h > 44:
            draw_rect(surf, C["panel"], (sx, log_top, sw, log_h), 8, 1, C["border"])
            draw_text(surf, T("log_title"), FONTS["xs"], C["text3"], bx2, log_top + 5)
            line_y = log_top + 22
            for msg_txt, mc in gs.log:
                if line_y + 16 > log_top + log_h - 6: break
                col_text = (C["gold2"] if mc == "W" else
                            C["text2"] if mc == "B" else C["text3"])
                s = msg_txt
                while FONTS["xs"].size(s)[0] > bw - 4 and len(s) > 4:
                    s = s[:-1]
                if len(s) < len(msg_txt): s = s[:-3] + "..."
                draw_text(surf, s, FONTS["xs"], col_text, bx2, line_y)
                line_y += 17

        self.btn_new.draw(surf)
    def _draw_promo(self, surf):
        ow = pygame.Surface((surf.get_width(), surf.get_height()), pygame.SRCALPHA)
        ow.fill((0,0,0,160))
        surf.blit(ow, (0,0))
        pw, ph = 320, 150
        px = (surf.get_width() - pw) // 2
        py = (surf.get_height() - ph) // 2
        draw_rect(surf, C["panel"], (px, py, pw, ph), 12, 2, C["border2"])
        draw_text(surf, T("choose_promo"), FONTS["med"], C["text"],
                  px + pw // 2, py + 18, "midtop")
        opts = ["Q","R","B","N"]
        bw = 56; gap = 12
        total = bw * 4 + gap * 3
        bx_start = px + (pw - total) // 2
        self.promo_buttons = []
        for i, t in enumerate(opts):
            p = t if self.gs.turn == "W" else t.lower()
            bx3 = bx_start + i * (bw + gap)
            btn_rect = pygame.Rect(bx3, py + 60, bw, bw)
            draw_rect(surf, C["btn"], btn_rect, 8, 1, C["border"])
            psurf = piece_surface(p, int(bw * 0.7))
            pr = psurf.get_rect(center=btn_rect.center)
            surf.blit(psurf, pr)
            self.promo_buttons.append((btn_rect, t))

    def _draw_status_overlay(self, surf):
        ow = pygame.Surface((surf.get_width(), surf.get_height()), pygame.SRCALPHA)
        ow.fill((0,0,0,180))
        surf.blit(ow, (0,0))
        bw, bh = 340, 170
        bx = (surf.get_width() - bw) // 2
        by = (surf.get_height() - bh) // 2
        draw_rect(surf, C["panel"], (bx, by, bw, bh), 14, 2, C["gold"])
        gs = self.gs
        if gs.winner:
            name = T("white") if gs.winner == "W" else T("black")
            draw_text(surf, T("winner", name), FONTS["big"], C["gold2"],
                      surf.get_width() // 2, by + 30, "midtop")
        else:
            draw_text(surf, T("draw"), FONTS["big"], C["text2"],
                      surf.get_width() // 2, by + 30, "midtop")
        btn = Button((surf.get_width()//2 - 80, by + 100, 160, 40),
                      T("new_game"), color=C["accent2"], hover_color=C["accent"])
        btn.draw(surf)
        self._gameover_btn = btn

    def handle(self, event):
        gs = self.gs
        if gs.promo_at:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, t in self.promo_buttons:
                    if rect.collidepoint(event.pos):
                        gs.promote(t)
                        if self.lan and self.lan.connected:
                            self.lan.send({"type":"promo","piece":t})
                        return
            return

        if gs.over:
            if self._gameover_btn:
                if event.type == pygame.MOUSEMOTION:
                    self._gameover_btn.update_hover(event.pos)
                if self._gameover_btn.clicked(event):
                    self.new_game()
            return

        if event.type == pygame.MOUSEMOTION:
            self.btn_roll.update_hover(event.pos)
            self.btn_end.update_hover(event.pos)
            self.btn_new.update_hover(event.pos)
            for btn, _ in self.res_buttons:
                btn.update_hover(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            rc = self.click_to_rc(*event.pos)
            if rc:
                r, c = rc
                if gs.sel:
                    mv = next((m for m in gs.legal if m[0] == r and m[1] == c), None)
                    if mv:
                        fr, fc = gs.sel
                        # Start slide animation
                        p = gs.board[fr][fc]
                        if p:
                            sq = self.sq
                            sx0 = self.bx + fc * sq + sq // 2
                            sy0 = self.by + fr * sq + sq // 2
                            ex0 = self.bx + mv[1] * sq + sq // 2
                            ey0 = self.by + mv[0] * sq + sq // 2
                            self.anim = PieceAnim(p, sx0, sy0, ex0, ey0)
                        self._last_move = (fr, fc, mv[0], mv[1])
                        gs.sel = None; gs.legal = []
                        gs.execute_move(fr, fc, *mv)
                        # Send move to LAN opponent
                        if self.lan and self.lan.connected:
                            self.lan.send({"type":"move",
                                           "fr":fr,"fc":fc,
                                           "tr":mv[0],"tc":mv[1],
                                           "sp":mv[2]})
                        return
                    gs.sel = None; gs.legal = []
                if gs.can_select(r, c):
                    # Block human input if it's the bot's or remote player's turn
                    is_bot_turn = self.bot_enabled and gs.turn == self.bot_color
                    is_lan_remote = (self.lan and self.lan.connected
                                     and gs.turn != self.lan.my_color)
                    if not is_bot_turn and not is_lan_remote:
                        gs.sel = (r, c)
                        gs.legal = legal_moves_for(gs.board, r, c, gs.ep, gs.castling, gs.turn)
                return

        is_bot_turn = self.bot_enabled and gs.turn == self.bot_color
        is_lan_remote = (self.lan and self.lan.connected
                         and gs.turn != self.lan.my_color)
        if not is_bot_turn and not is_lan_remote:
            if self.btn_roll.clicked(event):
                d1, d2 = gs.roll()
                if d1:
                    self.dice_vals = (d1, d2)
                    if self.lan and self.lan.connected:
                        self.lan.send({"type":"roll","d1":d1,"d2":d2})
            if self.btn_end.clicked(event):
                gs.end_turn()
                if self.lan and self.lan.connected:
                    self.lan.send({"type":"end_turn"})
        if self.btn_new.clicked(event):
            # Signal App to show mode screen
            self._request_mode_screen = True
        for btn, t in self.res_buttons:
            if btn.clicked(event):
                gs.resurrect(t)
                if self.lan and self.lan.connected:
                    self.lan.send({"type":"resurrect","piece":t})

    def tick(self):
        """Called every frame. Handles bot moves and LAN messages."""
        gs = self.gs

        # ── LAN receive ── process ALL pending messages ───────
        if self.lan and self.lan.connected:
            while True:
                msg = self.lan.poll()
                if msg is None:
                    break
                mtype = msg.get("type")
                if mtype == "move":
                    fr,fc,tr,tc = msg["fr"],msg["fc"],msg["tr"],msg["tc"]
                    sp = msg.get("sp")
                    p = gs.board[fr][fc]
                    if p and self.sq > 1:
                        sq = self.sq
                        self.anim = PieceAnim(p,
                            self.bx+fc*sq+sq//2, self.by+fr*sq+sq//2,
                            self.bx+tc*sq+sq//2, self.by+tr*sq+sq//2)
                    self._last_move = (fr,fc,tr,tc)
                    gs.execute_move(fr,fc,tr,tc,sp)
                elif mtype == "roll":
                    d1,d2 = msg["d1"],msg["d2"]
                    gs.crit = False; gs.crit_key = None; gs.crit_used = False
                    s = d1 + d2
                    if s == 12:
                        gs.crit = True; gs.od[gs.turn] = settings["crit_ap"]
                    elif s == 2:
                        gs.od[gs.turn] = max(0, s - settings["fail_penalty"])
                    else:
                        gs.od[gs.turn] = s
                    gs.rolled = True; gs.moved_pieces = {}; gs.act_used = 0
                    gs.phase = gs.detect_phase()
                    gs.check_start_of_turn()
                    self.dice_vals = (d1, d2)
                elif mtype == "end_turn":
                    gs.end_turn()
                elif mtype == "new_game":
                    self.new_game()
                elif mtype == "promo":
                    gs.promote(msg["piece"])
                elif mtype == "resurrect":
                    gs.resurrect(msg["piece"])

        # ── Bot tick ─────────────────────────────────────────
        if not self.bot_enabled or gs.over or gs.promo_at:
            return
        if gs.turn != self.bot_color:
            self._bot_pending = False
            return

        if not gs.rolled:
            # Bot rolls dice
            d1, d2 = gs.roll()
            if d1: self.dice_vals = (d1, d2)
            self._bot_delay = _time.monotonic() + 0.4
            self._bot_pending = True
            return

        if self._bot_pending and _time.monotonic() < self._bot_delay:
            return   # wait for delay

        # Bot makes a move
        mv = bot_pick_move(gs, self.bot_difficulty)
        if mv:
            fr, fc, tr, tc, sp = mv
            p = gs.board[fr][fc]
            if p:
                sq = self.sq
                self.anim = PieceAnim(p,
                    self.bx+fc*sq+sq//2, self.by+fr*sq+sq//2,
                    self.bx+tc*sq+sq//2, self.by+tr*sq+sq//2)
            self._last_move = (fr, fc, tr, tc)
            gs.execute_move(fr, fc, tr, tc, sp)
            # If bot used all actions or ran out of AP, end turn
            if (gs.act_used >= settings["max_actions"] or
                    not any(gs.can_select(r2, c2)
                            for r2 in range(8) for c2 in range(8))):
                self._bot_delay = _time.monotonic() + 0.5
                self._bot_pending = True
                # Schedule end turn in next tick
                self._end_turn_after = self._bot_delay
            else:
                self._bot_delay = _time.monotonic() + 0.35
                self._bot_pending = True
        else:
            # No move available, end turn
            gs.end_turn()
            self._bot_pending = False

        # Check if bot should end turn
        if hasattr(self, "_end_turn_after") and _time.monotonic() >= self._end_turn_after:
            if gs.rolled and gs.turn == self.bot_color:
                gs.end_turn()
            del self._end_turn_after

    def refresh_labels(self):
        self.btn_roll.label = T("roll_dice")
        self.btn_end.label  = T("end_turn")
        self.btn_new.label  = T("new_game")


# ─────────────────────────────────────────
#  AUTO-UPDATER
# ─────────────────────────────────────────
CURRENT_VERSION = "1.9.9"   # обновляй при каждом релизе / update on each release
GITHUB_REPO = "1GioiG1/Chess-of-Evil"   # ваш репозиторий

import urllib.request as _urllib_req
import subprocess as _subprocess
import tempfile as _tempfile
import shutil as _shutil

class UpdateChecker:
    def __init__(self):
        self.latest_version: str | None = None
        self.release_url: str = ""
        self.asset_url: str = ""
        self.checked = False
        self.checking = False
        self.check_error: str = ""
        self.downloading = False
        self.download_progress = 0.0     # 0.0 → 1.0
        self.download_error: str = ""
        self.ready_to_restart = False
        self._downloaded_path: str = ""
        self._thread: threading.Thread | None = None

    def start_check(self):
        if self.checking or self.checked:
            return
        self.checking = True
        self._thread = threading.Thread(target=self._check, daemon=True)
        self._thread.start()

    def _check(self):
        try:
            import ssl as _ssl
            api = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
            req = _urllib_req.Request(api, headers={
                "User-Agent": f"ChessOfEvil/{CURRENT_VERSION}",
                "Accept": "application/vnd.github+json",
            })

            # Try SSL contexts in order: certifi → default → unverified
            data = None
            last_err = ""
            for ctx_fn in [
                lambda: __import__("certifi") and _ssl.create_default_context(
                    cafile=__import__("certifi").where()),
                lambda: _ssl.create_default_context(),
                lambda: _ssl._create_unverified_context(),
            ]:
                try:
                    ctx = ctx_fn()
                    with _urllib_req.urlopen(req, timeout=12, context=ctx) as resp:
                        data = _json.loads(resp.read().decode("utf-8"))
                    break
                except Exception as e:
                    last_err = str(e)
                    continue

            if data is None:
                raise Exception(last_err)

            tag = data.get("tag_name", "")
            self.latest_version = tag.lstrip("v").strip()
            self.release_url = data.get("html_url", "")
            self.check_error = ""
            for asset in data.get("assets", []):
                if asset.get("name", "") == "main.py":
                    self.asset_url = asset.get("browser_download_url", "")
                    break
            if not self.asset_url:
                for asset in data.get("assets", []):
                    if asset.get("name", "").endswith(".exe"):
                        self.asset_url = asset.get("browser_download_url", "")
                        break
            if not self.asset_url:
                for asset in data.get("assets", []):
                    if "_Linux" in asset.get("name", ""):
                        self.asset_url = asset.get("browser_download_url", "")
                        break
        except Exception as e:
            self.latest_version = None
            self.check_error = str(e)
        finally:
            self.checked = True
            self.checking = False

    def update_available(self) -> bool:
        if not self.latest_version:
            return False
        try:
            # Strip any leading 'v', take only digits and dots
            import re as _re
            def parse_ver(s):
                s = s.strip().lstrip("v")
                parts = _re.findall(r'\d+', s)
                return tuple(int(x) for x in parts[:3]) if parts else (0,)
            cur = parse_ver(CURRENT_VERSION)
            lat = parse_ver(self.latest_version)
            return lat > cur
        except Exception:
            return False

    def start_download(self):
        """Start downloading the update in background thread."""
        if self.downloading or not self.asset_url:
            return
        self.downloading = True
        self.download_progress = 0.0
        self.download_error = ""
        t = threading.Thread(target=self._download, daemon=True)
        t.start()

    def _download(self):
        try:
            req = _urllib_req.Request(
                self.asset_url,
                headers={"User-Agent": "ChessOfEvil"}
            )
            with _urllib_req.urlopen(req, timeout=30) as resp:
                total = int(resp.headers.get("Content-Length", 0))
                # Write to temp file
                suffix = ".py" if self.asset_url.endswith(".py") else \
                         ".exe" if self.asset_url.endswith(".exe") else ""
                fd, tmp_path = _tempfile.mkstemp(suffix=suffix)
                received = 0
                with os.fdopen(fd, "wb") as f:
                    while True:
                        chunk = resp.read(65536)
                        if not chunk:
                            break
                        f.write(chunk)
                        received += len(chunk)
                        if total > 0:
                            self.download_progress = received / total
                self._downloaded_path = tmp_path
                self.download_progress = 1.0
                self.ready_to_restart = True
        except Exception as e:
            self.download_error = str(e)
        finally:
            self.downloading = False

    def apply_and_restart(self):
        """Replace current file and restart the process."""
        if not self.ready_to_restart or not self._downloaded_path:
            return
        try:
            if getattr(sys, "frozen", False):
                # PyInstaller .exe — можно заменить только после закрытия
                current_exe = sys.executable
                new_exe = self._downloaded_path

                # Создаём .bat файл который:
                # 1. Ждёт пока текущий процесс закроется
                # 2. Копирует новый .exe поверх старого
                # 3. Запускает новый .exe
                # 4. Удаляет себя
                bat_path = current_exe + "_update.bat"
                pid = os.getpid()
                bat_content = f"""@echo off
echo Ожидание завершения игры...
:wait
tasklist /FI "PID eq {pid}" 2>NUL | find /I "{pid}" >NUL
if not errorlevel 1 (
    timeout /t 1 /nobreak >NUL
    goto wait
)
echo Применение обновления...
timeout /t 1 /nobreak >NUL
copy /Y "{new_exe}" "{current_exe}"
del "{new_exe}"
start "" "{current_exe}"
del "%~f0"
"""
                with open(bat_path, "w", encoding="cp866") as f:
                    f.write(bat_content)

                # Запускаем батник скрыто и выходим
                _subprocess.Popen(
                    ["cmd.exe", "/C", bat_path],
                    creationflags=_subprocess.CREATE_NO_WINDOW
                    if hasattr(_subprocess, "CREATE_NO_WINDOW") else 0
                )
                pygame.quit()
                sys.exit(0)
            else:
                # Running as .py — можно заменить напрямую
                current_py = os.path.abspath(__file__)
                backup = current_py + ".bak"
                _shutil.copy2(current_py, backup)
                _shutil.copy2(self._downloaded_path, current_py)
                os.remove(self._downloaded_path)
                _subprocess.Popen([sys.executable, current_py] + sys.argv[1:])
                pygame.quit()
                sys.exit(0)
        except Exception as e:
            self.download_error = f"Ошибка применения обновления: {e}"
            self.ready_to_restart = False

_updater = UpdateChecker()


class ModeScreen:
    """Start screen: choose local, vs bot, or LAN."""

    DIFF_LABELS = {"easy": ("Простой","Easy"), "medium": ("Средний","Medium"), "hard": ("Сложный","Hard")}

    def __init__(self):
        self.lan_session: LanSession | None = None
        self.lan_state = "idle"   # idle | hosting | connecting | connected | error
        self.lan_ip_input = ""
        self.lan_my_ip = ""
        self.lan_error = ""
        self.result = None          # set when user picks a mode
        self.bot_difficulty = "medium"
        self._input_active = False
        self._cursor_blink = 0.0

    def draw(self, surf):
        sw, sh = surf.get_width(), surf.get_height()
        surf.fill(C["bg"])
        # Gradient
        for yy in range(0, sh, 4):
            t = yy / sh
            pygame.draw.line(surf, (int(18+t*8), int(18+t*5), int(24+t*14)), (0,yy),(sw,yy))

        cx = sw // 2
        # Title
        draw_text(surf, T("title"), FONTS["big"], C["gold2"], cx, 40, "midtop")
        pygame.draw.line(surf, C["border"], (cx-200, 76), (cx+200, 76), 1)

        card_w = min(sw - 80, 780)
        card_x = cx - card_w // 2

        # ── Local 2-player ─────────────────────────────
        section_y = 96
        draw_rect(surf, C["panel"], (card_x, section_y, card_w, 70), 10, 1, C["border"])
        lbl = "Два игрока за одним экраном" if LANG=="ru" else "Local 2-Player"
        draw_text(surf, lbl, FONTS["med"], C["text"], card_x+20, section_y+14)
        sub = "Оба игрока на этом компьютере" if LANG=="ru" else "Both players on this computer"
        draw_text(surf, sub, FONTS["sm"], C["text3"], card_x+20, section_y+36)
        btn_local = pygame.Rect(card_x + card_w - 140, section_y+16, 120, 36)
        draw_rect(surf, C["accent2"], btn_local, 8)
        lbl_s = "Играть" if LANG=="ru" else "Play"
        draw_text(surf, lbl_s, FONTS["med"], C["text"], btn_local.centerx, btn_local.centery, "center")
        self._btn_local = btn_local

        # ── vs Bot ─────────────────────────────────────
        section_y = 186
        draw_rect(surf, C["panel"], (card_x, section_y, card_w, 100), 10, 1, C["border"])
        lbl2 = "Против бота" if LANG=="ru" else "vs Bot"
        draw_text(surf, lbl2, FONTS["med"], C["text"], card_x+20, section_y+14)
        sub2 = "Сложность:" if LANG=="ru" else "Difficulty:"
        draw_text(surf, sub2, FONTS["sm"], C["text3"], card_x+20, section_y+38)

        # Difficulty buttons
        self._btn_diffs = {}
        diffs = ["easy", "medium", "hard"]
        for i, d in enumerate(diffs):
            lbl_d = self.DIFF_LABELS[d][0 if LANG=="ru" else 1]
            bx2 = card_x + 140 + i * 130
            br = pygame.Rect(bx2, section_y+32, 120, 30)
            active = d == self.bot_difficulty
            draw_rect(surf, C["accent2"] if active else C["btn"], br, 6)
            draw_text(surf, lbl_d, FONTS["sm"],
                      C["text"] if active else C["text2"],
                      br.centerx, br.centery, "center")
            self._btn_diffs[d] = br

        btn_bot = pygame.Rect(card_x + card_w - 140, section_y+32, 120, 36)
        draw_rect(surf, C["accent2"], btn_bot, 8)
        draw_text(surf, lbl_s, FONTS["med"], C["text"], btn_bot.centerx, btn_bot.centery, "center")
        self._btn_bot = btn_bot

        # ── LAN ────────────────────────────────────────
        section_y = 306
        lan_h = 160
        draw_rect(surf, C["panel"], (card_x, section_y, card_w, lan_h), 10, 1, C["border"])
        lbl3 = "Сетевая игра (LAN / Radmin)" if LANG=="ru" else "Network Play (LAN / Radmin)"
        draw_text(surf, lbl3, FONTS["med"], C["text"], card_x+20, section_y+14)

        if self.lan_state == "idle":
            # Host button
            btn_host = pygame.Rect(card_x+20, section_y+44, 180, 36)
            draw_rect(surf, C["btn"], btn_host, 8, 1, C["border2"])
            host_lbl = "Создать игру" if LANG=="ru" else "Host Game"
            draw_text(surf, host_lbl, FONTS["med"], C["text2"], btn_host.centerx, btn_host.centery, "center")
            self._btn_host = btn_host

            # IP input + connect
            ip_lbl = "IP хоста:" if LANG=="ru" else "Host IP:"
            draw_text(surf, ip_lbl, FONTS["sm"], C["text3"], card_x+220, section_y+50)
            ip_rect = pygame.Rect(card_x+310, section_y+44, 180, 32)
            border_c = C["accent"] if self._input_active else C["inp_border"]
            draw_rect(surf, C["inp_bg"], ip_rect, 6, 2, border_c)
            cursor = "|" if (self._input_active and int(_time.monotonic()*2) % 2) else ""
            draw_text(surf, self.lan_ip_input + cursor, FONTS["sm"], C["text"],
                      ip_rect.x+8, ip_rect.centery, "midleft")
            self._ip_rect = ip_rect

            btn_conn = pygame.Rect(card_x+500, section_y+44, 130, 36)
            draw_rect(surf, C["accent2"], btn_conn, 8)
            conn_lbl = "Подключиться" if LANG=="ru" else "Connect"
            draw_text(surf, conn_lbl, FONTS["sm"], C["text"], btn_conn.centerx, btn_conn.centery, "center")
            self._btn_conn = btn_conn

            sub3 = "Убедитесь что оба в одной сети (или Radmin VPN)" if LANG=="ru" else \
                   "Both players must be on the same network (or Radmin VPN)"
            draw_text(surf, sub3, FONTS["xs"], C["text3"], card_x+20, section_y+94)

        elif self.lan_state in ("hosting", "connecting"):
            spinner = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"[int(_time.monotonic()*8) % 10]
            if self.lan_state == "hosting":
                my_ip = self.lan_session.get_local_ip() if self.lan_session else "..."
                msg = f"{spinner}  Ожидание подключения...  IP: {my_ip}" if LANG=="ru" else \
                      f"{spinner}  Waiting for opponent...  Your IP: {my_ip}"
            else:
                msg = f"{spinner}  Подключение к {self.lan_ip_input}..." if LANG=="ru" else \
                      f"{spinner}  Connecting to {self.lan_ip_input}..."
            draw_text(surf, msg, FONTS["med"], C["text2"], cx, section_y+70, "center")
            btn_cancel = pygame.Rect(cx-60, section_y+110, 120, 32)
            draw_rect(surf, C["btn"], btn_cancel, 6)
            draw_text(surf, "Отмена" if LANG=="ru" else "Cancel", FONTS["sm"], C["text"],
                      btn_cancel.centerx, btn_cancel.centery, "center")
            self._btn_cancel = btn_cancel

        elif self.lan_state == "connected":
            role = "Хост (Белые)" if (self.lan_session and self.lan_session.role == NetworkRole.HOST) else "Гость (Чёрные)"
            role_en = "Host (White)" if (self.lan_session and self.lan_session.role == NetworkRole.HOST) else "Guest (Black)"
            msg = f"✓  Соединение установлено!  {role}" if LANG=="ru" else f"✓  Connected!  {role_en}"
            draw_text(surf, msg, FONTS["med"], (80,200,80), cx, section_y+50, "center")
            btn_start = pygame.Rect(cx-80, section_y+90, 160, 36)
            draw_rect(surf, C["accent2"], btn_start, 8)
            draw_text(surf, "Начать игру" if LANG=="ru" else "Start Game",
                      FONTS["med"], C["text"], btn_start.centerx, btn_start.centery, "center")
            self._btn_start_lan = btn_start

        elif self.lan_state == "error":
            draw_text(surf, f"✗  {self.lan_error}", FONTS["sm"], C["red2"], cx, section_y+50, "center")
            btn_retry = pygame.Rect(cx-60, section_y+90, 120, 32)
            draw_rect(surf, C["btn"], btn_retry, 6)
            draw_text(surf, "Назад" if LANG=="ru" else "Back", FONTS["sm"], C["text"],
                      btn_retry.centerx, btn_retry.centery, "center")
            self._btn_cancel = btn_retry

        # Check connection status change
        if self.lan_session and self.lan_session.connected and self.lan_state in ("hosting","connecting"):
            self.lan_state = "connected"
        if self.lan_session and self.lan_session.error and self.lan_state in ("hosting","connecting"):
            self.lan_error = self.lan_session.error
            self.lan_state = "error"

        # ── Version / Update bar at bottom ─────────────
        ver_y = sh - 36
        draw_text(surf, f"v{CURRENT_VERSION}", FONTS["xs"], C["text3"], 14, ver_y + 8, "topleft")
        self._btn_update = None  # reset each frame

        if _updater.download_error:
            err_short = _updater.download_error[:70]
            draw_text(surf, f"✗ {err_short}", FONTS["xs"], C["red2"], cx, ver_y + 8, "midtop")

        elif _updater.ready_to_restart:
            lbl = "✓  Готово — нажмите для перезапуска" if LANG=="ru" else "✓  Done — click to restart"
            bw2 = FONTS["med"].size(lbl)[0] + 28
            btn_r = pygame.Rect(cx - bw2 // 2, ver_y - 2, bw2, 32)
            draw_rect(surf, (30, 100, 50), btn_r, 6, 2, (60, 200, 100))
            draw_text(surf, lbl, FONTS["med"], (120, 255, 150), btn_r.centerx, btn_r.centery, "center")
            self._btn_update = btn_r

        elif _updater.downloading:
            prog = _updater.download_progress
            pct = int(prog * 100)
            lbl = f"⬇  {'Скачивание' if LANG=='ru' else 'Downloading'} {pct}%..."
            draw_text(surf, lbl, FONTS["sm"], C["text2"], cx, ver_y + 2, "midtop")
            bar_w2 = 260
            bx2 = cx - bar_w2 // 2
            pygame.draw.rect(surf, C["bg3"], (bx2, ver_y + 22, bar_w2, 6), border_radius=3)
            pygame.draw.rect(surf, C["accent"], (bx2, ver_y + 22, int(bar_w2 * prog), 6), border_radius=3)

        elif _updater.update_available():
            has_direct = bool(_updater.asset_url)
            if has_direct:
                lbl = f"⬆  {'Доступна' if LANG=='ru' else 'Update'} v{_updater.latest_version} — {'скачать и обновить' if LANG=='ru' else 'download & update'}"
            else:
                lbl = f"⬆  {'Доступна' if LANG=='ru' else 'Update'} v{_updater.latest_version} — {'открыть страницу' if LANG=='ru' else 'open page'}"
            bw2 = FONTS["sm"].size(lbl)[0] + 28
            btn_u = pygame.Rect(cx - bw2 // 2, ver_y, bw2, 30)
            draw_rect(surf, (35, 70, 35), btn_u, 6, 1, (70, 150, 70))
            draw_text(surf, lbl, FONTS["sm"], (130, 220, 130), btn_u.centerx, btn_u.centery, "center")
            self._btn_update = btn_u

        elif _updater.checking:
            draw_text(surf, "Проверка обновлений..." if LANG=="ru" else "Checking for updates...",
                      FONTS["xs"], C["text3"], cx, ver_y + 8, "midtop")
        elif _updater.checked:
            if _updater.check_error:
                # Show short actual error for debugging
                err = _updater.check_error
                short = err[:55] if len(err) > 55 else err
                draw_text(surf, f"⚠ {short}",
                          FONTS["xs"], C["text3"], cx, ver_y + 8, "midtop")
            else:
                draw_text(surf, f"✓ Актуальная версия (v{CURRENT_VERSION})" if LANG=="ru" else f"✓ Up to date (v{CURRENT_VERSION})",
                          FONTS["xs"], C["text3"], cx, ver_y + 8, "midtop")

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            # Update button — behaviour depends on state
            if hasattr(self, "_btn_update") and self._btn_update and self._btn_update.collidepoint(pos):
                if _updater.ready_to_restart:
                    _updater.apply_and_restart()
                elif _updater.update_available():
                    if _updater.asset_url and not _updater.downloading:
                        _updater.start_download()
                    elif _updater.release_url:
                        import webbrowser
                        webbrowser.open(_updater.release_url)
            # Local play
            if hasattr(self, "_btn_local") and self._btn_local.collidepoint(pos):
                self.result = {"mode": "local"}
            # Difficulty selection
            if hasattr(self, "_btn_diffs"):
                for d, br in self._btn_diffs.items():
                    if br.collidepoint(pos):
                        self.bot_difficulty = d
            # vs Bot
            if hasattr(self, "_btn_bot") and self._btn_bot.collidepoint(pos):
                self.result = {"mode": "bot", "difficulty": self.bot_difficulty}
            # LAN buttons
            if self.lan_state == "idle":
                if hasattr(self, "_btn_host") and self._btn_host.collidepoint(pos):
                    sess = LanSession(); sess.start_host()
                    self.lan_session = sess; self.lan_state = "hosting"
                if hasattr(self, "_ip_rect") and self._ip_rect.collidepoint(pos):
                    self._input_active = True
                else:
                    if hasattr(self, "_ip_rect"):
                        self._input_active = False
                if hasattr(self, "_btn_conn") and self._btn_conn.collidepoint(pos):
                    if self.lan_ip_input.strip():
                        sess = LanSession(); sess.start_client(self.lan_ip_input.strip())
                        self.lan_session = sess; self.lan_state = "connecting"
            elif self.lan_state in ("hosting","connecting","error"):
                if hasattr(self, "_btn_cancel") and self._btn_cancel.collidepoint(pos):
                    if self.lan_session: self.lan_session.close()
                    self.lan_session = None; self.lan_state = "idle"; self.lan_error = ""
            elif self.lan_state == "connected":
                if hasattr(self, "_btn_start_lan") and self._btn_start_lan.collidepoint(pos):
                    self.result = {"mode": "lan", "session": self.lan_session}

        if event.type == pygame.KEYDOWN and self._input_active:
            if event.key == pygame.K_BACKSPACE:
                self.lan_ip_input = self.lan_ip_input[:-1]
            elif event.key == pygame.K_RETURN:
                self._input_active = False
            elif len(self.lan_ip_input) < 15 and (event.unicode.isdigit() or event.unicode == "."):
                self.lan_ip_input += event.unicode
        return None


class App:
    def __init__(self):
        self.W, self.H = 1100, 700
        self.MIN_W, self.MIN_H = 900, 600

        # Set pygame icon (32x32) BEFORE display.set_mode — affects taskbar on some OS
        _icon_set = False
        for _iname in ["icon_32.png", "icon_48.png", "icon_256.png"]:
            _ipath = resource_path(f"assets/{_iname}")
            if os.path.exists(_ipath):
                try:
                    _isurf = pygame.image.load(_ipath).convert_alpha()
                    _i32 = pygame.transform.smoothscale(_isurf, (32, 32))
                    pygame.display.set_icon(_i32)
                    _icon_set = True
                    break
                except Exception:
                    continue

        self.screen = pygame.display.set_mode((self.W, self.H), pygame.RESIZABLE)
        pygame.display.set_caption("Chess of Evil")
        self.clock = pygame.time.Clock()

        # Win32 API: set high-quality icon (256px) in window title bar
        # This overrides pygame's 32x32 limitation on Windows
        self._set_win32_icon()

        load_fonts()
        clear_piece_cache()

        self.tab = "game"
        self.tabs = ["game", "settings", "learn"]
        self.tab_label_keys = {"game":"tab_game","settings":"tab_settings","learn":"tab_learn"}
        self.TAB_H = 44

        self.game_screen = GameScreen()
        self.settings_screen = SettingsScreen()
        self.tutorial_screen = TutorialScreen()
        self.mode_screen = ModeScreen()
        self.btn_lang = Button((0,0,90,32), "EN / РУ", font=FONTS["sm"],
                                color=C["bg3"], hover_color=C["btn_hover"])
        self.show_mode_screen = True  # show on first launch
        _updater.start_check()  # async update check

    def _set_win32_icon(self):
        """Set high-quality 256px window icon via Win32 API (Windows only)."""
        try:
            import ctypes
            WM_SETICON  = 0x0080
            ICON_SMALL  = 0
            ICON_BIG    = 1
            IMAGE_ICON  = 1
            LR_LOADFROMFILE = 0x10

            ico_path = resource_path("assets/icon.ico")
            if not os.path.exists(ico_path):
                return

            user32 = ctypes.windll.user32

            # Load icons at specific sizes
            hbig = user32.LoadImageW(
                None, ico_path, IMAGE_ICON, 256, 256, LR_LOADFROMFILE)
            hsmall = user32.LoadImageW(
                None, ico_path, IMAGE_ICON, 16, 16, LR_LOADFROMFILE)

            # Get window handle from pygame
            info = pygame.display.get_wm_info()
            hwnd = info.get("window")
            if not hwnd:
                return

            if hbig:
                user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, hbig)
            if hsmall:
                user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, hsmall)

        except Exception:
            pass  # Non-Windows — skip silently

    def _active_tabs(self):
        """Return tabs to show based on current state."""
        if self.show_mode_screen:
            return ["settings", "learn"]   # mode screen: settings + tutorial only
        gs = self.game_screen.gs
        if gs.game_started and not gs.over:
            return ["game"]               # during game: only Game tab
        return ["game", "settings", "learn"]  # pre/post game: all tabs

    def draw_tabs(self):
        surf = self.screen
        lang_w = 96
        lang_margin = 6
        self.btn_lang.rect = pygame.Rect(self.W - lang_w - lang_margin, 6, lang_w, 32)
        self.btn_lang.draw(surf)

        active_tabs = self._active_tabs()
        if not active_tabs:
            pygame.draw.line(surf, C["border"], (0, self.TAB_H), (self.W, self.TAB_H), 1)
            return

        tabs_right = self.W - lang_w - lang_margin * 2 - 8
        tabs_left = 8
        n = len(active_tabs)
        gap = 6
        tab_w = (tabs_right - tabs_left - gap * (n - 1)) // n
        for i, t in enumerate(active_tabs):
            tx = tabs_left + i * (tab_w + gap)
            ty = 7
            th = self.TAB_H - 14
            is_active = (t == self.tab) or (self.show_mode_screen and t == self.tab)
            bg = C["tab_active"] if is_active else C["bg3"]
            draw_rect(surf, bg, (tx, ty, tab_w, th), 8,
                      1 if is_active else 0, C["border"])
            draw_text(surf, T(self.tab_label_keys[t]), FONTS["med"],
                      C["text"] if is_active else C["text2"],
                      tx + tab_w // 2, ty + th // 2, "center")
        pygame.draw.line(surf, C["border"], (0, self.TAB_H), (self.W, self.TAB_H), 1)

    def handle_tabs(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if y < self.TAB_H:
                active_tabs = self._active_tabs()
                if not active_tabs:
                    return False
                lang_w = 96; lang_margin = 6
                tabs_right = self.W - lang_w - lang_margin * 2 - 8
                tabs_left = 8; n = len(active_tabs); gap = 6
                tab_w = (tabs_right - tabs_left - gap * (n - 1)) // n
                for i, t in enumerate(active_tabs):
                    tx = tabs_left + i * (tab_w + gap)
                    if tx <= x <= tx + tab_w:
                        self.tab = t; return True
        return False

    def run(self):
        global LANG
        running = True
        while running:
            self.clock.tick(60)

            # ── Mode selection screen ─────────────────────────
            if self.show_mode_screen:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False; break
                    if event.type == pygame.VIDEORESIZE:
                        self.W = max(event.w, self.MIN_W)
                        self.H = max(event.h, self.MIN_H)
                        self.screen = pygame.display.set_mode((self.W, self.H), pygame.RESIZABLE)
                        clear_piece_cache()
                    # Lang button
                    if event.type == pygame.MOUSEMOTION:
                        self.btn_lang.update_hover(event.pos)
                    if self.btn_lang.clicked(event):
                        LANG = "en" if LANG == "ru" else "ru"
                        self.game_screen.refresh_labels()
                        self.settings_screen.refresh_labels()
                        self.tutorial_screen.refresh_labels()
                    # "← Menu" back button (shown over settings/tutorial)
                    if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                            and self.tab in ("settings", "learn")
                            and hasattr(self, "_back_btn_rect")
                            and self._back_btn_rect
                            and self._back_btn_rect.collidepoint(event.pos)):
                        self.tab = "game"
                        continue
                    # Tab bar
                    if self.handle_tabs(event):
                        continue
                    ev_offset = self._offset_event(event, 0, -self.TAB_H)
                    # Route to appropriate screen based on active tab
                    if self.tab == "settings":
                        self.settings_screen.handle(ev_offset)
                    elif self.tab == "learn":
                        res = self.tutorial_screen.handle(ev_offset)
                        if res == "exit":
                            self.tab = "game"
                    else:
                        # Mode selection screen
                        self.mode_screen.handle(ev_offset)
                    if self.mode_screen.result:
                        r = self.mode_screen.result
                        self.mode_screen.result = None
                        if r["mode"] == "local":
                            self.game_screen.bot_enabled = False
                            self.game_screen.lan = None
                        elif r["mode"] == "bot":
                            self.game_screen.bot_enabled = True
                            self.game_screen.bot_color = "B"
                            self.game_screen.bot_difficulty = r["difficulty"]
                            self.game_screen.lan = None
                        elif r["mode"] == "lan":
                            sess = r["session"]
                            self.game_screen.lan = sess
                            self.game_screen.bot_enabled = False
                            if sess.role == NetworkRole.HOST:
                                sess.my_color = "W"
                            else:
                                sess.my_color = "B"
                        self.game_screen.new_game()
                        self.show_mode_screen = False
                        self.tab = "game"

                self.screen.fill(C["bg"])
                self.draw_tabs()
                sub = pygame.Surface((self.W, self.H - self.TAB_H))
                if self.tab == "settings":
                    self.settings_screen.locked = False
                    self.settings_screen.draw(sub)
                elif self.tab == "learn":
                    self.tutorial_screen.draw(sub)
                else:
                    self.tab = "game"
                    self.mode_screen.draw(sub)

                # Blit content first
                self.screen.blit(sub, (0, self.TAB_H))

                # "← Меню" button drawn AFTER blit so it appears on top
                if self.tab in ("settings", "learn"):
                    back_lbl = "← Меню" if LANG == "ru" else "← Menu"
                    back_w = FONTS["med"].size(back_lbl)[0] + 20
                    back_h = 32
                    back_rect = pygame.Rect(12, self.H - back_h - 12, back_w, back_h)
                    draw_rect(self.screen, C["bg2"], back_rect, 8, 1, C["border2"])
                    draw_text(self.screen, back_lbl, FONTS["med"], C["text"],
                              back_rect.centerx, back_rect.centery, "center")
                    self._back_btn_rect = back_rect
                else:
                    self._back_btn_rect = None

                pygame.display.flip()
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.VIDEORESIZE:
                    self.W = max(event.w, self.MIN_W)
                    self.H = max(event.h, self.MIN_H)
                    self.screen = pygame.display.set_mode((self.W, self.H), pygame.RESIZABLE)
                    clear_piece_cache()

                if self.handle_tabs(event):
                    continue

                if event.type == pygame.MOUSEMOTION:
                    self.btn_lang.update_hover(event.pos)
                if self.btn_lang.clicked(event):
                    LANG = "en" if LANG == "ru" else "ru"
                    self.game_screen.refresh_labels()
                    self.settings_screen.refresh_labels()
                    self.tutorial_screen.refresh_labels()

                ev = self._offset_event(event, 0, -self.TAB_H)
                if self.tab == "game":
                    self.game_screen.handle(ev)
                elif self.tab == "settings":
                    self.settings_screen.handle(ev)
                elif self.tab == "learn":
                    result = self.tutorial_screen.handle(ev)
                    if result == "exit":
                        self.tab = "game"

            # Bot / LAN tick (outside event loop, called every frame)
            if self.tab == "game" and not self.show_mode_screen:
                self.game_screen.tick()
                # New Game button was clicked → show mode screen
                if self.game_screen._request_mode_screen:
                    self.game_screen._request_mode_screen = False
                    self.show_mode_screen = True
                    self.mode_screen.lan_state = "idle"
                    self.mode_screen.result = None

            self.screen.fill(C["bg"])
            sub_w = self.W
            sub_h = self.H - self.TAB_H
            sub_surf = pygame.Surface((sub_w, sub_h))
            gs = self.game_screen.gs
            # Lock settings as soon as dice are rolled (not just after first move)
            in_active_game = gs.rolled or gs.game_started and not gs.over
            self.settings_screen.locked = in_active_game
            # Force game tab during active game
            if in_active_game and self.tab != "game":
                self.tab = "game"
            # Draw tabs AFTER forcing tab
            self.draw_tabs()
            if self.tab == "game":
                self.game_screen.draw(sub_surf)
            elif self.tab == "settings":
                self.settings_screen.draw(sub_surf)
            elif self.tab == "learn":
                self.tutorial_screen.draw(sub_surf)
            self.screen.blit(sub_surf, (0, self.TAB_H))
            pygame.display.flip()

        # Cleanup
        if self.game_screen.lan:
            self.game_screen.lan.close()
        pygame.quit()
        sys.exit()


    def _offset_event(self, event, dx, dy):
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            ne = pygame.event.Event(event.type, dict(event.__dict__))
            if hasattr(ne, "pos"):
                ne.pos = (ne.pos[0] + dx, ne.pos[1] + dy)
            return ne
        return event


if __name__ == "__main__":
    App().run()
