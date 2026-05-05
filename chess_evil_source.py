"""
Шахматы Зла / Chess of Evil
Pygame desktop application
"""

import pygame
import sys
import random
import math
import json
import os
import copy

pygame.init()
pygame.font.init()

# ─────────────────────────────────────────
#  LOCALISATION
# ─────────────────────────────────────────
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
        "language": "Язык / Language",
        "settings_title": "Настройки игры",
        "cost_move": "Стоимость хода (ОД)",
        "cost_res": "Стоимость воскрешения (ОД)",
        "res_count": "Количество воскрешений",
        "max_actions": "Макс. действий за ход",
        "crit_bonus": "ОД при крите (12)",
        "fail_penalty": "Штраф при неудаче (2)",
        "save_settings": "Сохранить",
        "reset_settings": "Сбросить",
        "pieces": {"K": "Король", "Q": "Ферзь", "R": "Ладья", "B": "Слон", "N": "Конь", "P": "Пешка"},
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
        "fail_msg": "Критическая неудача! −1 ОД.",
        "roll_prompt": "Бросьте кубики",
        "choose_promo": "Выберите фигуру",
        "resurrect": "Воскрешение",
        "res_btn": "{} ({}ОД)",
        "log_takes": "{} берёт {}",
        "log_move": "{} → {}",
        "log_castle": "Рокировка",
        "log_ep": "Взятие на проходе",
        "log_promo": "Превращение → {}",
        "log_res": "Воскрешение: {} → {}",
        "log_newgame": "Новая игра! Ход белых.",
        "log_turn": "Ход {}. Бросьте кубики.",
        "learn_title": "Обучение",
        "learn_next": "Далее →",
        "learn_prev": "← Назад",
        "learn_skip": "Пропустить туториал",
        "learn_restart": "Начать заново",
        "learn_exit": "Выйти в меню",
        "unlimited": "∞",
        "times": "раз",
    },
    "en": {
        "title": "Chess of Evil",
        "tab_game": "Game",
        "tab_settings": "Settings",
        "tab_learn": "Tutorial",
        "new_game": "New Game",
        "roll_dice": "Roll 2d6",
        "end_turn": "End Turn",
        "language": "Язык / Language",
        "settings_title": "Game Settings",
        "cost_move": "Move Cost (AP)",
        "cost_res": "Resurrect Cost (AP)",
        "res_count": "Resurrect Count",
        "max_actions": "Max Actions/Turn",
        "crit_bonus": "AP on Crit (12)",
        "fail_penalty": "Fail Penalty (2)",
        "save_settings": "Save",
        "reset_settings": "Reset",
        "pieces": {"K": "King", "Q": "Queen", "R": "Rook", "B": "Bishop", "N": "Knight", "P": "Pawn"},
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
        "fail_msg": "Critical Fail! −1 AP.",
        "roll_prompt": "Roll the dice",
        "choose_promo": "Choose a piece",
        "resurrect": "Resurrect",
        "res_btn": "{} ({}AP)",
        "log_takes": "{} takes {}",
        "log_move": "{} → {}",
        "log_castle": "Castling",
        "log_ep": "En passant",
        "log_promo": "Promotion → {}",
        "log_res": "Resurrect: {} → {}",
        "log_newgame": "New game! White's turn.",
        "log_turn": "{}'s turn. Roll dice.",
        "learn_title": "Tutorial",
        "learn_next": "Next →",
        "learn_prev": "← Back",
        "learn_skip": "Skip Tutorial",
        "learn_restart": "Restart",
        "learn_exit": "Back to Menu",
        "unlimited": "∞",
        "times": "x",
    }
}

def T(key, *args):
    s = STRINGS[LANG].get(key, key)
    if args:
        s = s.format(*args)
    return s

def TP(key):
    return STRINGS[LANG]["pieces"].get(key, key)

# ─────────────────────────────────────────
#  COLOURS & THEME
# ─────────────────────────────────────────
C = {
    "bg":          (18, 18, 24),
    "bg2":         (28, 28, 36),
    "bg3":         (38, 38, 50),
    "border":      (60, 60, 80),
    "border2":     (80, 80, 110),
    "text":        (230, 230, 240),
    "text2":       (160, 160, 180),
    "text3":       (100, 100, 120),
    "accent":      (90, 140, 220),
    "accent2":     (60, 100, 180),
    "green":       (60, 170, 90),
    "red":         (200, 60, 60),
    "red2":        (240, 80, 80),
    "gold":        (210, 170, 60),
    "gold2":       (240, 200, 80),
    "sq_light":    (240, 217, 181),
    "sq_dark":     (181, 136, 99),
    "sq_sel":      (90, 140, 220),
    "sq_can":      (90, 180, 90),
    "sq_cap":      (200, 80, 80),
    "sq_check":    (220, 60, 60),
    "panel":       (24, 24, 32),
    "panel2":      (32, 32, 44),
    "btn":         (40, 40, 56),
    "btn_hover":   (55, 55, 75),
    "btn_active":  (80, 120, 200),
    "btn_dis":     (30, 30, 40),
    "die_bg":      (35, 35, 50),
    "die_crit":    (40, 100, 40),
    "die_fail":    (120, 30, 30),
    "tab_active":  (50, 80, 160),
    "tab_hover":   (40, 40, 58),
    "inp_bg":      (30, 30, 44),
    "inp_border":  (70, 70, 100),
}

# ─────────────────────────────────────────
#  DEFAULT SETTINGS
# ─────────────────────────────────────────
DEFAULT_SETTINGS = {
    "move_cost":  {"K": 8, "Q": 6, "R": 5, "B": 3, "N": 3, "P": 1},
    "res_cost":   {"K": 8, "Q": 6, "R": 5, "B": 3, "N": 3, "P": 1},
    "res_count":  {"K": 0, "Q": 1, "R": -1, "B": -1, "N": -1, "P": 0},
    # -1 = unlimited, 0 = cannot be resurrected
    "max_actions": 3,
    "crit_ap": 12,
    "fail_penalty": 1,
    "castle_cost": 5,  # rook price by rule
}

settings = copy.deepcopy(DEFAULT_SETTINGS)

# ─────────────────────────────────────────
#  PIECE DATA
# ─────────────────────────────────────────
SYM_W = {"K": "♔", "Q": "♕", "R": "♖", "B": "♗", "N": "♘", "P": "♙"}
SYM_B = {"K": "♚", "Q": "♛", "R": "♜", "B": "♝", "N": "♞", "P": "♟"}

def sym(p):
    t = p.upper()
    return SYM_W[t] if p.isupper() else SYM_B[t]

def is_white(p): return p and p == p.upper()
def tp(p): return p.upper() if p else None
def pc(p): return "W" if is_white(p) else "B"
def opp(c): return "B" if c == "W" else "W"
def in_b(r, c): return 0 <= r < 8 and 0 <= c < 8
def f2l(c): return chr(97 + c)
def coord_str(r, c): return f"{f2l(c)}{8 - r}"

# ─────────────────────────────────────────
#  CHESS ENGINE
# ─────────────────────────────────────────

def raw_moves(board, r, c, ep, castling, skip_castle=False):
    p = board[r][c]
    if not p:
        return []
    t = tp(p)
    mine = pc(p)
    enemy = opp(mine)
    dir_ = -1 if is_white(p) else 1
    moves = []

    def push(tr, tc, sp=None):
        if not in_b(tr, tc):
            return False
        tgt = board[tr][tc]
        if tgt and pc(tgt) == mine:
            return False
        moves.append((tr, tc, sp))
        return not tgt

    def slide(dr, dc):
        rr, cc = r + dr, c + dc
        while in_b(rr, cc):
            if not push(rr, cc):
                break
            rr += dr
            cc += dc

    if t == "P":
        start = 6 if is_white(p) else 1
        if in_b(r + dir_, c) and not board[r + dir_][c]:
            moves.append((r + dir_, c, None))
            if r == start and not board[r + 2 * dir_][c]:
                moves.append((r + 2 * dir_, c, None))
        for dc in (-1, 1):
            nr, nc = r + dir_, c + dc
            if not in_b(nr, nc):
                continue
            if board[nr][nc] and pc(board[nr][nc]) == enemy:
                moves.append((nr, nc, None))
            if ep and ep == (nr, nc):
                moves.append((nr, nc, "ep"))

    if t == "N":
        for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
            push(r + dr, c + dc)

    if t in ("B", "Q"):
        for dr, dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
            slide(dr, dc)

    if t in ("R", "Q"):
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            slide(dr, dc)

    if t == "K":
        for dr, dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            push(r + dr, c + dc)
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
    if not kp:
        return False
    return attacked_by(board, kp[0], kp[1], opp(color), ep, castling)


def apply_raw(board, fr, fc, tr, tc, sp):
    b = [row[:] for row in board]
    p = b[fr][fc]
    captured = b[tr][tc]
    b[tr][tc] = p
    b[fr][fc] = None
    if sp == "ep":
        er = tr + 1 if is_white(p) else tr - 1
        captured = b[er][tc]
        b[er][tc] = None
    if sp == "ck":
        b[tr][5] = b[tr][7]
        b[tr][7] = None
    if sp == "cq":
        b[tr][3] = b[tr][0]
        b[tr][0] = None
    return b, captured


def legal_moves_for(board, r, c, ep, castling, color):
    p = board[r][c]
    if not p or pc(p) != color:
        return []
    result = []
    for tr, tc, sp in raw_moves(board, r, c, ep, castling):
        if sp in ("ck", "cq"):
            mid_c = 5 if sp == "ck" else 3
            tmp = [row[:] for row in board]
            tmp[r][c] = None
            if in_check(tmp, color, ep, castling):
                continue
            tmp2 = [row[:] for row in board]
            tmp2[r][mid_c] = p
            tmp2[r][c] = None
            if in_check(tmp2, color, ep, castling):
                continue
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

# ─────────────────────────────────────────
#  GAME STATE
# ─────────────────────────────────────────

def fresh_board():
    board = [[None]*8 for _ in range(8)]
    for c, p in enumerate("RNBQKBNR"):
        board[0][c] = p.lower()
        board[7][c] = p
    for c in range(8):
        board[1][c] = "p"
        board[6][c] = "P"
    return board


class GameState:
    def __init__(self):
        self.board = fresh_board()
        self.turn = "W"
        self.od = {"W": 0, "B": 0}
        self.rolled = False
        self.act_used = 0
        self.moved_pieces = {}   # key(r,c) -> times moved this turn
        self.crit = False
        self.crit_key = None
        self.crit_used = False
        self.phase = "normal"
        self.castling = {"W": {"k": True, "q": True}, "B": {"k": True, "q": True}}
        self.ep = None
        self.dead = {"W": [], "B": []}         # list of uppercase type chars
        self.queen_res = {"W": 0, "B": 0}      # how many times queen resurrected
        self.res_counts = {"W": {}, "B": {}}   # t -> times resurrected
        self.sel = None
        self.legal = []
        self.over = False
        self.winner = None      # "W"|"B"|None
        self.promo_at = None
        self.check_sq = None
        self.log = []
        self.dice = (0, 0)

    def add_log(self, msg, color="sys"):
        self.log.insert(0, (msg, color))
        if len(self.log) > 60:
            self.log.pop()

    def detect_phase(self):
        pieces = all_pieces(self.board)
        w_nk = [x for x in pieces if pc(x[0]) == "W" and tp(x[0]) != "K"]
        b_nk = [x for x in pieces if pc(x[0]) == "B" and tp(x[0]) != "K"]
        if not w_nk and not b_nk:
            return "clash"
        active_nk = w_nk if self.turn == "W" else b_nk
        if not active_nk:
            return "gambit"
        return "normal"

    def move_cost(self, p, r, c):
        t = tp(p)
        color = pc(p)
        if t == "K":
            if in_check(self.board, color, self.ep, self.castling):
                return self.od[color]
            if self.phase == "gambit" and color == self.turn:
                return 1
            return settings["move_cost"]["K"]
        return settings["move_cost"][t]

    def castle_cost(self):
        return settings["castle_cost"]

    def piece_key(self, r, c):
        return r * 8 + c

    def times_moved(self, r, c):
        return self.moved_pieces.get(self.piece_key(r, c), 0)

    def can_select(self, r, c):
        if not self.rolled or self.over or self.promo_at:
            return False
        if self.act_used >= settings["max_actions"]:
            return False
        p = self.board[r][c]
        if not p or pc(p) != self.turn:
            return False
        cost = self.move_cost(p, r, c)
        if self.od[self.turn] < cost:
            return False
        times = self.times_moved(r, c)
        if times >= 1:
            if not self.crit or self.crit_used:
                return False
            if self.crit_key is not None and self.crit_key != self.piece_key(r, c):
                return False
            if times >= 2:
                return False
        return bool(legal_moves_for(self.board, r, c, self.ep, self.castling, self.turn))

    def execute_move(self, fr, fc, tr, tc, sp):
        p = self.board[fr][fc]
        t = tp(p)
        color = self.turn

        cost = self.castle_cost() if sp in ("ck", "cq") else self.move_cost(p, fr, fc)
        self.od[color] -= cost
        self.act_used += 1

        src_key = self.piece_key(fr, fc)
        dst_key = self.piece_key(tr, tc)
        src_times = self.moved_pieces.get(src_key, 0)
        self.moved_pieces.pop(src_key, None)
        self.moved_pieces[dst_key] = src_times + 1

        if self.crit and not self.crit_used:
            if src_times == 0:
                if self.crit_key is None:
                    self.crit_key = dst_key
            else:
                if self.crit_key == dst_key:
                    self.crit_used = True

        b2, captured = apply_raw(self.board, fr, fc, tr, tc, sp)
        self.board = b2

        self.ep = None
        if t == "P" and abs(tr - fr) == 2:
            self.ep = (fr + (1 if tr > fr else -1), fc)

        if t == "K":
            self.castling[color] = {"k": False, "q": False}
        if t == "R":
            if fc == 0: self.castling[color]["q"] = False
            if fc == 7: self.castling[color]["k"] = False
        if captured and tp(captured) == "R":
            ec = pc(captured)
            if tc == 0: self.castling[ec]["q"] = False
            if tc == 7: self.castling[ec]["k"] = False

        note = ""
        if sp == "ck" or sp == "cq":
            note = f" ({T('log_castle')})"
        elif sp == "ep":
            note = f" ({T('log_ep')})"

        if captured:
            self.add_log(T("log_takes", sym(p), sym(captured)) + note, color)
            self.dead[pc(captured)].append(tp(captured))
        else:
            self.add_log(T("log_move", sym(p), coord_str(tr, tc)) + note, color)

        if t == "P" and (tr == 0 or tr == 7):
            self.promo_at = (tr, tc)
            return

        self.after_move()

    def after_move(self):
        self.sel = None
        self.legal = []
        self.phase = self.detect_phase()
        enemy = opp(self.turn)
        kp = king_pos(self.board, enemy)
        self.check_sq = kp if in_check(self.board, enemy, self.ep, self.castling) else None

    def promote(self, piece_type):
        r, c = self.promo_at
        p = piece_type if self.turn == "W" else piece_type.lower()
        self.board[r][c] = p
        self.dead[self.turn].append("P")
        self.add_log(T("log_promo", sym(p)), self.turn)
        self.promo_at = None
        self.after_move()

    def check_start_of_turn(self):
        color = self.turn
        chk = in_check(self.board, color, self.ep, self.castling)
        any_legal = has_any_legal(self.board, color, self.ep, self.castling)
        if chk and not any_legal:
            self.over = True
            self.winner = opp(color)
            self.add_log(T("checkmate"), "sys")
            return False
        if not chk and not any_legal:
            self.over = True
            self.winner = None
            self.add_log(T("stalemate"), "sys")
            return False
        self.check_sq = king_pos(self.board, color) if chk else None
        return True

    def roll(self):
        if self.rolled or self.over:
            return None, None
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        s = d1 + d2
        self.dice = (d1, d2)
        self.crit = False
        self.crit_key = None
        self.crit_used = False

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

        self.rolled = True
        self.moved_pieces = {}
        self.act_used = 0
        self.phase = self.detect_phase()
        self.check_start_of_turn()
        return d1, d2

    def end_turn(self):
        if not self.rolled or self.over:
            return
        self.turn = opp(self.turn)
        self.rolled = False
        self.act_used = 0
        self.moved_pieces = {}
        self.crit = False
        self.crit_key = None
        self.crit_used = False
        self.od[self.turn] = 0
        self.sel = None
        self.legal = []
        self.check_sq = None
        self.add_log(T("log_turn", T("white") if self.turn=="W" else T("black")), "sys")

    def get_resurrectable(self):
        if self.phase != "clash" or not self.rolled or self.over:
            return []
        if self.act_used >= settings["max_actions"]:
            return []
        seen = {}
        for t in self.dead[self.turn]:
            if t in seen:
                continue
            max_r = settings["res_count"].get(t, -1)
            if max_r == 0:
                continue
            used = self.res_counts[self.turn].get(t, 0)
            if max_r != -1 and used >= max_r:
                continue
            cost = settings["res_cost"].get(t, settings["move_cost"].get(t, 1))
            if self.od[self.turn] < cost:
                continue
            seen[t] = cost
        return list(seen.items())

    def resurrect(self, t):
        if self.act_used >= settings["max_actions"]:
            return
        cost = settings["res_cost"].get(t, settings["move_cost"].get(t, 1))
        if self.od[self.turn] < cost:
            return
        p = t if self.turn == "W" else t.lower()
        orig = self._orig_positions(p)
        placed = None
        for r, c in orig:
            if not self.board[r][c]:
                self.board[r][c] = p
                placed = (r, c)
                break
        if not placed:
            br, bc = orig[0]
            cands = [(br+dr, bc+dc)
                     for dr in range(-3, 4) for dc in range(-3, 4)
                     if in_b(br+dr, bc+dc) and not self.board[br+dr][bc+dc]]
            if cands:
                pick = random.choice(cands)
                self.board[pick[0]][pick[1]] = p
                placed = pick
        if not placed:
            self.add_log("No free squares!", "sys")
            return
        self.od[self.turn] -= cost
        self.act_used += 1
        idx = self.dead[self.turn].index(t)
        self.dead[self.turn].pop(idx)
        self.res_counts[self.turn][t] = self.res_counts[self.turn].get(t, 0) + 1
        self.phase = self.detect_phase()
        self.add_log(T("log_res", sym(p), coord_str(placed[0], placed[1])), self.turn)

    def _orig_positions(self, p):
        t = tp(p)
        row = 7 if is_white(p) else 0
        return {
            "K": [(row, 4)],
            "Q": [(row, 3)],
            "R": [(row, 0), (row, 7)],
            "B": [(row, 2), (row, 5)],
            "N": [(row, 1), (row, 6)],
            "P": [(row, c) for c in range(8)],
        }.get(t, [(row, 4)])


# ─────────────────────────────────────────
#  FONTS
# ─────────────────────────────────────────
def load_fonts():
    global F_PIECE, F_BIG, F_MED, F_SM, F_XS, F_COORD
    # Try to find a unicode-capable font
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    ]
    font_path = None
    for fp in candidates:
        if os.path.exists(fp):
            font_path = fp
            break

    def mf(size):
        if font_path:
            return pygame.font.Font(font_path, size)
        return pygame.font.SysFont("segoeuisymbol,symbola,dejavusans", size)

    F_PIECE = mf(36)
    F_BIG   = mf(22)
    F_MED   = mf(16)
    F_SM    = mf(13)
    F_XS    = mf(11)
    F_COORD = mf(10)

# ─────────────────────────────────────────
#  UI HELPERS
# ─────────────────────────────────────────

def draw_rect(surf, color, rect, radius=6, border=0, border_color=None):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surf, border_color, rect, border, border_radius=radius)

def draw_text(surf, text, font, color, x, y, anchor="topleft", max_width=None):
    if max_width:
        # word wrap
        words = text.split()
        lines = []
        line = ""
        for w in words:
            test = (line + " " + w).strip()
            if font.size(test)[0] <= max_width:
                line = test
            else:
                if line:
                    lines.append(line)
                line = w
        if line:
            lines.append(line)
        total_h = len(lines) * (font.get_height() + 2)
        base_y = y
        if anchor == "center":
            base_y = y - total_h // 2
        for i, l in enumerate(lines):
            s = font.render(l, True, color)
            r = s.get_rect()
            if anchor == "center":
                r.midtop = (x, base_y + i * (font.get_height() + 2))
            else:
                r.topleft = (x, base_y + i * (font.get_height() + 2))
            surf.blit(s, r)
        return total_h
    else:
        s = font.render(text, True, color)
        r = s.get_rect()
        setattr(r, anchor, (x, y))
        surf.blit(s, r)
        return r.height

class Button:
    def __init__(self, rect, label, font=None, color=None, hover_color=None,
                 text_color=None, disabled_color=None, radius=8):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.font = font or F_MED
        self.color = color or C["btn"]
        self.hover_color = hover_color or C["btn_hover"]
        self.text_color = text_color or C["text"]
        self.disabled_color = disabled_color or C["btn_dis"]
        self.radius = radius
        self.hovered = False
        self.disabled = False
        self.active = False

    def draw(self, surf):
        if self.disabled:
            bg = self.disabled_color
            tc = C["text3"]
        elif self.active:
            bg = C["btn_active"]
            tc = C["text"]
        elif self.hovered:
            bg = self.hover_color
            tc = self.text_color
        else:
            bg = self.color
            tc = self.text_color
        draw_rect(surf, bg, self.rect, self.radius, 1, C["border"])
        s = self.font.render(self.label, True, tc)
        r = s.get_rect(center=self.rect.center)
        surf.blit(s, r)

    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not self.disabled and self.rect.collidepoint(event.pos):
                return True
        return False

class Spinner:
    """Integer spinner with +/- buttons"""
    def __init__(self, rect, value, min_val, max_val, label="", allow_unlimited=False):
        self.rect = pygame.Rect(rect)
        self.value = value
        self.min_val = min_val
        self.max_val = max_val
        self.label = label
        self.allow_unlimited = allow_unlimited  # -1 means unlimited
        bw = 24
        self.btn_minus = pygame.Rect(rect[0], rect[1], bw, rect[3])
        self.btn_plus  = pygame.Rect(rect[0]+rect[2]-bw, rect[1], bw, rect[3])
        self.val_rect  = pygame.Rect(rect[0]+bw, rect[1], rect[2]-2*bw, rect[3])

    def draw(self, surf):
        draw_rect(surf, C["inp_bg"], self.rect, 6, 1, C["inp_border"])
        draw_rect(surf, C["btn"], self.btn_minus, 6)
        draw_rect(surf, C["btn"], self.btn_plus, 6)
        draw_text(surf, "−", F_MED, C["text"], self.btn_minus.centerx, self.btn_minus.centery, "center")
        draw_text(surf, "+", F_MED, C["text"], self.btn_plus.centerx, self.btn_plus.centery, "center")
        val_str = T("unlimited") if (self.allow_unlimited and self.value == -1) else str(self.value)
        draw_text(surf, val_str, F_MED, C["text"], self.val_rect.centerx, self.val_rect.centery, "center")

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_minus.collidepoint(event.pos):
                if self.allow_unlimited and self.value == self.min_val:
                    self.value = -1
                elif self.value == -1:
                    pass
                elif self.value > self.min_val:
                    self.value -= 1
                return True
            if self.btn_plus.collidepoint(event.pos):
                if self.value == -1:
                    self.value = self.min_val
                elif self.value < self.max_val:
                    self.value += 1
                return True
        return False

# ─────────────────────────────────────────
#  BOARD RENDERER
# ─────────────────────────────────────────

class BoardRenderer:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.sq = size // 8
        self.anim_pieces = {}   # key -> (surf, cx, cy, tx, ty, t, dur)
        self.highlight_sq = {}  # (r,c) -> color, alpha

    def sq_rect(self, r, c):
        return pygame.Rect(self.x + c * self.sq, self.y + r * self.sq, self.sq, self.sq)

    def click_to_rc(self, mx, my):
        if not (self.x <= mx < self.x + self.size and self.y <= my < self.y + self.size):
            return None
        c = (mx - self.x) // self.sq
        r = (my - self.y) // self.sq
        return (r, c)

    def draw(self, surf, gs):
        for r in range(8):
            for c in range(8):
                light = (r + c) % 2 == 0
                base = C["sq_light"] if light else C["sq_dark"]
                rect = self.sq_rect(r, c)

                # check highlight
                if gs.check_sq and (r, c) == gs.check_sq:
                    col_sq = C["sq_check"]
                elif gs.sel and (r, c) == gs.sel:
                    col_sq = C["sq_sel"]
                elif gs.legal and any(tr == r and tc == c for tr, tc, _ in gs.legal):
                    if gs.board[r][c]:
                        col_sq = C["sq_cap"]
                    else:
                        col_sq = C["sq_can"]
                else:
                    col_sq = base

                pygame.draw.rect(surf, col_sq, rect)

                # dot for possible moves
                if gs.legal and any(tr == r and tc == c for tr, tc, _ in gs.legal) and not gs.board[r][c]:
                    cx, cy = rect.center
                    pygame.draw.circle(surf, (*C["sq_can"], 180), (cx, cy), self.sq // 8)

                # coordinates
                if r == 7:
                    draw_text(surf, f2l(c), F_COORD, C["text3"] if light else C["sq_light"],
                              rect.right - 3, rect.bottom - 2, "bottomright")
                if c == 0:
                    draw_text(surf, str(8 - r), F_COORD, C["text3"] if light else C["sq_light"],
                              rect.left + 2, rect.top + 1)

                # piece
                p = gs.board[r][c]
                if p:
                    s = F_PIECE.render(sym(p), True, (240, 240, 250) if is_white(p) else (20, 20, 20))
                    shadow = F_PIECE.render(sym(p), True, (0,0,0,120))
                    sr = s.get_rect(center=rect.center)
                    surf.blit(shadow, sr.move(1, 1))
                    surf.blit(s, sr)

        # board border
        pygame.draw.rect(surf, C["border2"],
                         (self.x-1, self.y-1, self.size+2, self.size+2), 2, border_radius=4)


# ─────────────────────────────────────────
#  DIE RENDERER
# ─────────────────────────────────────────
DIE_DOTS = {
    1: [(0.5, 0.5)],
    2: [(0.25, 0.25), (0.75, 0.75)],
    3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
    4: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)],
    5: [(0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)],
    6: [(0.25, 0.2), (0.75, 0.2), (0.25, 0.5), (0.75, 0.5), (0.25, 0.8), (0.75, 0.8)],
}

def draw_die(surf, val, rect, crit=False, fail=False):
    bg = C["die_crit"] if crit else C["die_fail"] if fail else C["die_bg"]
    border = (80, 180, 80) if crit else (200, 80, 80) if fail else C["border2"]
    draw_rect(surf, bg, rect, 8, 2, border)
    if val < 1 or val > 6:
        draw_text(surf, "?", F_MED, C["text2"], rect.centerx, rect.centery, "center")
        return
    dot_color = (220, 240, 200) if crit else (240, 180, 180) if fail else C["text"]
    r = max(3, rect.width // 10)
    for fx, fy in DIE_DOTS[val]:
        cx = int(rect.x + fx * rect.width)
        cy = int(rect.y + fy * rect.height)
        pygame.draw.circle(surf, dot_color, (cx, cy), r)


# ─────────────────────────────────────────
#  SETTINGS SCREEN
# ─────────────────────────────────────────
PIECE_TYPES = ["K", "Q", "R", "B", "N", "P"]

class SettingsScreen:
    def __init__(self, sw, sh):
        self.sw = sw
        self.sh = sh
        self.scroll = 0
        self.spinners = {}
        self.global_spinners = {}
        self.btn_save = Button((sw//2-100, sh-60, 200, 36), T("save_settings"),
                                color=C["accent2"], hover_color=C["accent"])
        self.btn_reset = Button((sw//2+110, sh-60, 140, 36), T("reset_settings"))
        self.dirty = False
        self._build()

    def _build(self):
        self.spinners = {}
        x0 = 60
        col_w = (self.sw - 120) // 3
        row_h = 36
        start_y = 130

        for i, t in enumerate(PIECE_TYPES):
            y = start_y + i * (row_h + 10)
            self.spinners[("move", t)] = Spinner(
                (x0 + col_w, y, col_w - 20, row_h),
                settings["move_cost"][t], 1, 20)
            self.spinners[("res_cost", t)] = Spinner(
                (x0 + col_w * 2, y, col_w - 20, row_h),
                settings["res_cost"][t], 1, 20)
            max_r = settings["res_count"][t]
            self.spinners[("res_count", t)] = Spinner(
                (x0 + col_w * 3 - 20, y, col_w - 20, row_h),
                max_r, 0, 10, allow_unlimited=True)

        gy = start_y + len(PIECE_TYPES) * (row_h + 10) + 20
        self.global_spinners["max_actions"] = Spinner(
            (x0 + col_w, gy, col_w - 20, row_h), settings["max_actions"], 1, 10)
        self.global_spinners["crit_ap"] = Spinner(
            (x0 + col_w, gy + row_h + 10, col_w - 20, row_h), settings["crit_ap"], 1, 20)
        self.global_spinners["fail_penalty"] = Spinner(
            (x0 + col_w, gy + 2*(row_h + 10), col_w - 20, row_h), settings["fail_penalty"], 0, 5)
        self.global_spinners["castle_cost"] = Spinner(
            (x0 + col_w, gy + 3*(row_h + 10), col_w - 20, row_h), settings["castle_cost"], 1, 20)

    def draw(self, surf):
        surf.fill(C["bg"])
        draw_text(surf, T("settings_title"), F_BIG, C["text"], self.sw//2, 24, "midtop")

        x0 = 60
        col_w = (self.sw - 120) // 3
        row_h = 36
        start_y = 130

        # headers
        for j, hdr in enumerate([T("cost_move"), T("cost_res"), T("res_count")]):
            draw_text(surf, hdr, F_SM, C["text2"], x0 + col_w*(j+1), 100, "midtop")

        for i, t in enumerate(PIECE_TYPES):
            y = start_y + i * (row_h + 10)
            draw_text(surf, TP(t), F_MED, C["text"], x0, y + row_h//2, "midleft")
            for key in [("move", t), ("res_cost", t), ("res_count", t)]:
                self.spinners[key].draw(surf)

        gy = start_y + len(PIECE_TYPES) * (row_h + 10) + 20
        pygame.draw.line(surf, C["border"], (x0, gy - 8), (self.sw - x0, gy - 8))
        labels = [T("max_actions"), T("crit_bonus"), T("fail_penalty"), "Стоимость рокировки"]
        for j, (k, lbl) in enumerate(zip(
            ["max_actions","crit_ap","fail_penalty","castle_cost"], labels)):
            yy = gy + j * (row_h + 10)
            draw_text(surf, lbl, F_MED, C["text"], x0, yy + row_h//2, "midleft")
            self.global_spinners[k].draw(surf)

        self.btn_save.draw(surf)
        self.btn_reset.draw(surf)

    def handle(self, event):
        for sp in self.spinners.values():
            sp.handle(event)
        for sp in self.global_spinners.values():
            sp.handle(event)
        if self.btn_save.handle(event):
            self._apply()
            return "saved"
        if self.btn_reset.handle(event):
            self._reset()
            return "reset"
        if event.type == pygame.MOUSEMOTION:
            self.btn_save.hovered = self.btn_save.rect.collidepoint(event.pos)
            self.btn_reset.hovered = self.btn_reset.rect.collidepoint(event.pos)
        return None

    def _apply(self):
        for t in PIECE_TYPES:
            settings["move_cost"][t] = self.spinners[("move", t)].value
            settings["res_cost"][t] = self.spinners[("res_cost", t)].value
            settings["res_count"][t] = self.spinners[("res_count", t)].value
        for k in ["max_actions","crit_ap","fail_penalty","castle_cost"]:
            settings[k] = self.global_spinners[k].value

    def _reset(self):
        global settings
        settings = copy.deepcopy(DEFAULT_SETTINGS)
        self._build()

    def refresh_labels(self):
        self.btn_save.label = T("save_settings")
        self.btn_reset.label = T("reset_settings")


# ─────────────────────────────────────────
#  TUTORIAL
# ─────────────────────────────────────────
TUTORIAL_STEPS_RU = [
    {
        "title": "Добро пожаловать в Шахматы Зла!",
        "text": (
            "Это шахматы с элементом удачи. В начале каждого хода вы бросаете 2 кубика (2к6) "
            "и получаете Очки Действий (ОД). Чем больше ОД — тем больше фигур вы можете "
            "переместить за один ход."
        ),
        "highlight": None,
    },
    {
        "title": "Цены фигур",
        "text": (
            "Каждый ход фигуры стоит ОД:\n\n"
            "♔ Король — 8 ОД\n"
            "♕ Ферзь — 6 ОД\n"
            "♖ Ладья — 5 ОД\n"
            "♗ Слон — 3 ОД\n"
            "♘ Конь — 3 ОД\n"
            "♙ Пешка — 1 ОД\n\n"
            "Рокировка стоит 5 ОД (цена ладьи)."
        ),
        "highlight": None,
    },
    {
        "title": "Ограничения хода",
        "text": (
            "За один ход вы можете:\n"
            "• Сделать не более 3 действий\n"
            "• Каждая фигура ходит только 1 раз\n"
            "• Тратить ОД пока они не кончатся\n\n"
            "Если ОД меньше, чем стоит фигура — она недоступна для хода."
        ),
        "highlight": None,
    },
    {
        "title": "Критические броски",
        "text": (
            "Бросок 12 (максимум) — Критическая удача!\n"
            "Одна выбранная фигура может сходить дважды за ход.\n\n"
            "Бросок 2 (минимум) — Критическая неудача!\n"
            "Вы теряете 1 ОД из полученных."
        ),
        "highlight": None,
    },
    {
        "title": "Шах и ход короля",
        "text": (
            "Когда ваш король под шахом — он подсвечивается красным.\n\n"
            "Ход короля под шахом стоит ВСЕ ваши ОД, независимо от их количества.\n\n"
            "Если у вас мало ОД, это может быть проблемой!"
        ),
        "highlight": None,
    },
    {
        "title": "Королевский Гамбит",
        "text": (
            "Если у вас остался только Король — активируется Королевский Гамбит.\n\n"
            "В этом режиме ход короля стоит всего 1 ОД "
            "(но не более 3 ходов за раз — стандартное ограничение).\n\n"
            "Ваш одинокий король становится гораздо мобильнее!"
        ),
        "highlight": None,
    },
    {
        "title": "Столкновение Судеб",
        "text": (
            "Если у ОБОИХ игроков остались только Короли — начинается Столкновение Судеб!\n\n"
            "Теперь можно тратить ОД на воскрешение мёртвых фигур. "
            "Воскрешённая фигура появляется на своей стартовой позиции.\n\n"
            "Пешки воскресить нельзя. Ферзь воскрешается лишь раз."
        ),
        "highlight": None,
    },
    {
        "title": "Завершение игры",
        "text": (
            "Игра заканчивается:\n"
            "• Матом — король противника не может спастись\n"
            "• Патом — у противника нет ходов, но шаха нет (ничья)\n\n"
            "Удачи в игре! Возвращайтесь сюда в любой момент "
            "через вкладку «Обучение»."
        ),
        "highlight": None,
    },
]

TUTORIAL_STEPS_EN = [
    {
        "title": "Welcome to Chess of Evil!",
        "text": (
            "This is chess with a luck element. At the start of each turn you roll 2d6 "
            "and receive Action Points (AP). The more AP you get, the more pieces you "
            "can move in one turn."
        ),
        "highlight": None,
    },
    {
        "title": "Piece Costs",
        "text": (
            "Each piece move costs AP:\n\n"
            "♔ King — 8 AP\n"
            "♕ Queen — 6 AP\n"
            "♖ Rook — 5 AP\n"
            "♗ Bishop — 3 AP\n"
            "♘ Knight — 3 AP\n"
            "♙ Pawn — 1 AP\n\n"
            "Castling costs 5 AP (rook price)."
        ),
        "highlight": None,
    },
    {
        "title": "Turn Limits",
        "text": (
            "Each turn you may:\n"
            "• Take at most 3 actions\n"
            "• Each piece moves only once\n"
            "• Spend AP until they run out\n\n"
            "If AP is less than a piece's cost — that piece is unavailable."
        ),
        "highlight": None,
    },
    {
        "title": "Critical Rolls",
        "text": (
            "Roll 12 (maximum) — Critical Hit!\n"
            "One chosen piece may move twice this turn.\n\n"
            "Roll 2 (minimum) — Critical Fail!\n"
            "You lose 1 AP from the total rolled."
        ),
        "highlight": None,
    },
    {
        "title": "Check & King Move",
        "text": (
            "When your king is in check it is highlighted in red.\n\n"
            "Moving the king while in check costs ALL your remaining AP, "
            "regardless of how much you have.\n\n"
            "Having few AP when in check can be very dangerous!"
        ),
        "highlight": None,
    },
    {
        "title": "Royal Gambit",
        "text": (
            "If only your King remains — Royal Gambit activates!\n\n"
            "In this mode the king's move costs just 1 AP "
            "(still limited to 3 actions per turn).\n\n"
            "Your lone king becomes much more mobile!"
        ),
        "highlight": None,
    },
    {
        "title": "Clash of Fates",
        "text": (
            "If BOTH players have only Kings — Clash of Fates begins!\n\n"
            "You can now spend AP to resurrect dead pieces. "
            "A resurrected piece appears on its starting square.\n\n"
            "Pawns cannot be resurrected. Queens can only be resurrected once."
        ),
        "highlight": None,
    },
    {
        "title": "End of Game",
        "text": (
            "The game ends by:\n"
            "• Checkmate — the opponent's king cannot escape\n"
            "• Stalemate — the opponent has no moves but isn't in check (draw)\n\n"
            "Good luck! Come back here any time "
            "via the Tutorial tab."
        ),
        "highlight": None,
    },
]

class TutorialScreen:
    def __init__(self, sw, sh):
        self.sw = sw
        self.sh = sh
        self.step = 0
        self.btn_next = Button((sw//2+20, sh-70, 180, 40), T("learn_next"),
                                color=C["accent2"], hover_color=C["accent"])
        self.btn_prev = Button((sw//2-200, sh-70, 180, 40), T("learn_prev"))
        self.btn_exit = Button((sw-160, sh-70, 140, 40), T("learn_exit"))

    def steps(self):
        return TUTORIAL_STEPS_RU if LANG == "ru" else TUTORIAL_STEPS_EN

    def draw(self, surf):
        surf.fill(C["bg"])
        steps = self.steps()
        total = len(steps)
        step = steps[self.step]

        # Progress bar
        bar_w = self.sw - 120
        bar_h = 6
        bx = 60
        by = 60
        draw_rect(surf, C["bg3"], (bx, by, bar_w, bar_h), 3)
        prog_w = int(bar_w * (self.step + 1) / total)
        draw_rect(surf, C["accent"], (bx, by, prog_w, bar_h), 3)

        # Step counter
        draw_text(surf, f"{self.step+1} / {total}", F_SM, C["text3"], self.sw//2, by-18, "center")

        # Card
        card_x = 80
        card_y = 90
        card_w = self.sw - 160
        card_h = self.sh - 190
        draw_rect(surf, C["panel"], (card_x, card_y, card_w, card_h), 12, 1, C["border"])

        # Title
        draw_text(surf, step["title"], F_BIG, C["gold2"], self.sw//2, card_y + 28, "midtop")

        # Divider
        pygame.draw.line(surf, C["border"], (card_x+20, card_y+62), (card_x+card_w-20, card_y+62))

        # Text (multiline)
        text_surf = pygame.Surface((card_w - 80, card_h - 100), pygame.SRCALPHA)
        text_surf.fill((0,0,0,0))
        lines = step["text"].split("\n")
        ty = 0
        for line in lines:
            if line.strip() == "":
                ty += 8
                continue
            wrapped = []
            words = line.split()
            cur = ""
            for w in words:
                test = (cur + " " + w).strip()
                if F_MED.size(test)[0] <= card_w - 80:
                    cur = test
                else:
                    if cur:
                        wrapped.append(cur)
                    cur = w
            if cur:
                wrapped.append(cur)
            for wline in wrapped:
                s = F_MED.render(wline, True, C["text"])
                text_surf.blit(s, (0, ty))
                ty += F_MED.get_height() + 3

        surf.blit(text_surf, (card_x + 40, card_y + 78))

        # Step illustration (simple icon)
        icons = ["🎲","♟","⚡","🎯","♔","🏆","⚔","🏁"]
        if self.step < len(icons):
            try:
                icon_surf = F_PIECE.render(icons[self.step], True, C["gold"])
                surf.blit(icon_surf, (card_x + card_w - 70, card_y + 20))
            except:
                pass

        # Buttons
        self.btn_prev.disabled = self.step == 0
        self.btn_next.label = T("learn_next") if self.step < total-1 else T("learn_exit")
        self.btn_prev.draw(surf)
        self.btn_next.draw(surf)
        self.btn_exit.draw(surf)

    def handle(self, event):
        steps = self.steps()
        if self.btn_next.handle(event):
            if self.step < len(steps) - 1:
                self.step += 1
            else:
                return "exit"
        if self.btn_prev.handle(event):
            if self.step > 0:
                self.step -= 1
        if self.btn_exit.handle(event):
            return "exit"
        for btn in [self.btn_next, self.btn_prev, self.btn_exit]:
            if event.type == pygame.MOUSEMOTION:
                btn.hovered = btn.rect.collidepoint(event.pos)
        return None

    def refresh_labels(self):
        self.btn_next.label = T("learn_next")
        self.btn_prev.label = T("learn_prev")
        self.btn_exit.label = T("learn_exit")


# ─────────────────────────────────────────
#  GAME SCREEN
# ─────────────────────────────────────────
class GameScreen:
    def __init__(self, sw, sh):
        self.sw = sw
        self.sh = sh
        self.gs = GameState()
        self.gs.add_log(T("log_newgame"), "sys")

        # Board
        board_size = min(sh - 40, sw - 300)
        bx = 20
        by = (sh - board_size) // 2
        self.board_r = BoardRenderer(bx, by, board_size)

        # Sidebar
        self.sx = bx + board_size + 16
        self.sy = 20
        self.sw2 = sw - self.sx - 10

        # Buttons
        bw = self.sw2 - 20
        bx2 = self.sx + 10
        self.btn_roll = Button((bx2, self.sy+120, bw, 38), T("roll_dice"),
                                color=C["accent2"], hover_color=C["accent"])
        self.btn_end  = Button((bx2, self.sy+164, bw, 38), T("end_turn"))
        self.btn_new  = Button((bx2, sh-50, bw, 36), T("new_game"),
                                color=C["btn"], hover_color=C["btn_hover"])

        self.promo_buttons = []
        self.res_buttons = []
        self.anim_dice = []
        self.dice_vals = (0, 0)
        self.dice_anim_t = 0

    def new_game(self):
        self.gs = GameState()
        self.gs.add_log(T("log_newgame"), "sys")
        self.dice_vals = (0, 0)

    def draw(self, surf):
        surf.fill(C["bg"])
        gs = self.gs

        # Board
        self.board_r.draw(surf, gs)

        # Sidebar
        sx = self.sx
        sy = self.sy
        sw2 = self.sw2
        bx2 = sx + 10

        # Player panels
        for i, color in enumerate(["W", "B"]):
            py = sy + i * 58
            is_active = gs.turn == color and not gs.over
            bg = C["panel2"] if is_active else C["panel"]
            border = C["accent"] if is_active else C["border"]
            draw_rect(surf, bg, (sx, py, sw2, 52), 8, 2, border)

            name = T("white") if color == "W" else T("black")
            draw_text(surf, ("♔ " if color=="W" else "♚ ") + name, F_MED, C["text"], bx2, py+8)
            od_val = gs.od[color]
            od_str = f"{od_val} {T('ap_label')}"
            draw_text(surf, od_str, F_BIG, C["gold2"] if is_active else C["text2"],
                      sx + sw2 - 10, py + 10, "topright")

            # OD bar
            bar_w = sw2 - 20
            bar_h = 6
            draw_rect(surf, C["bg3"], (bx2, py+38, bar_w, bar_h), 3)
            fill_w = int(bar_w * min(1.0, od_val / 12))
            fill_c = C["red2"] if od_val <= 2 else C["accent"]
            if fill_w > 0:
                draw_rect(surf, fill_c, (bx2, py+38, fill_w, bar_h), 3)

        # Phase label
        phase_labels = {
            "normal": T("phase_normal"),
            "gambit": T("phase_gambit"),
            "clash":  T("phase_clash"),
        }
        phase_lbl = phase_labels.get(gs.phase, "")
        phase_col = C["gold2"] if gs.phase != "normal" else C["text2"]
        draw_text(surf, phase_lbl, F_SM, phase_col, sx + sw2//2, sy+118, "midtop")

        # Dice
        die_size = 40
        gap = 12
        total_dice_w = 2 * die_size + gap
        dx = sx + (sw2 - total_dice_w) // 2
        dy = sy + 210
        d1, d2 = self.dice_vals
        crit = (d1+d2 == 12) and d1 > 0
        fail = (d1+d2 == 2) and d1 > 0
        draw_die(surf, d1, pygame.Rect(dx, dy, die_size, die_size), crit, fail)
        draw_die(surf, d2, pygame.Rect(dx+die_size+gap, dy, die_size, die_size), crit, fail)

        # Actions info
        acts_str = T("actions_label", gs.act_used, settings["max_actions"])
        if gs.crit and not gs.crit_used:
            acts_str += " ★"
        acts_col = C["gold2"] if gs.crit and not gs.crit_used else C["text2"]
        draw_text(surf, acts_str if gs.rolled else T("roll_prompt"),
                  F_SM, acts_col, sx+sw2//2, sy+260, "midtop")

        # Buttons
        self.btn_roll.disabled = gs.rolled or gs.over
        self.btn_end.disabled  = not gs.rolled or gs.over
        self.btn_roll.draw(surf)
        self.btn_end.draw(surf)

        # Resurrection buttons
        if gs.phase == "clash" and gs.rolled and not gs.over:
            self._draw_resurrect(surf, sy + 315)

        # Promo overlay
        if gs.promo_at:
            self._draw_promo(surf)

        # Status message
        if gs.over:
            self._draw_status(surf)
        elif gs.check_sq:
            enemy = opp(gs.turn)
            chk_name = T("white") if enemy=="W" else T("black")
            self._draw_msg(surf, f"♔ {T('check')} ({chk_name})", C["red2"])
        elif gs.phase == "gambit" and gs.rolled:
            self._draw_msg(surf, "⚡ " + T("phase_gambit"), C["gold"])
        elif gs.phase == "clash" and gs.rolled:
            self._draw_msg(surf, "⚔ " + T("phase_clash"), C["accent"])

        # Log
        log_y = self.sh - 160
        draw_rect(surf, C["panel"], (sx, log_y, sw2, 150), 8, 1, C["border"])
        draw_text(surf, "Log" if LANG=="en" else "Журнал", F_XS, C["text3"], bx2, log_y+6)
        for i, (msg, mc) in enumerate(gs.log[:7]):
            col_text = C["gold2"] if mc=="W" else C["text2"] if mc=="B" else C["text3"]
            if log_y + 22 + i*20 > log_y + 140:
                break
            draw_text(surf, msg[:40], F_XS, col_text, bx2, log_y + 22 + i * 20)

        # New game button
        self.btn_new.draw(surf)

    def _draw_resurrect(self, surf, start_y):
        gs = self.gs
        items = gs.get_resurrectable()
        if not items:
            return
        bx2 = self.sx + 10
        bw = self.sw2 - 20
        draw_text(surf, T("resurrect"), F_SM, C["text2"], bx2, start_y)
        self.res_buttons = []
        for i, (t, cost) in enumerate(items):
            p = t if gs.turn == "W" else t.lower()
            label = T("res_btn", sym(p) + " " + TP(t), cost)
            y = start_y + 20 + i * 42
            btn = Button((bx2, y, bw, 36), label, color=C["bg3"], hover_color=C["panel2"])
            btn.disabled = gs.act_used >= settings["max_actions"] or gs.od[gs.turn] < cost
            btn.draw(surf)
            self.res_buttons.append((btn, t))

    def _draw_promo(self, surf):
        ow = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        ow.fill((0, 0, 0, 160))
        surf.blit(ow, (0, 0))
        pw, ph = 300, 140
        px = (self.sw - pw) // 2
        py = (self.sh - ph) // 2
        draw_rect(surf, C["panel"], (px, py, pw, ph), 12, 2, C["border2"])
        draw_text(surf, T("choose_promo"), F_MED, C["text"], px+pw//2, py+16, "midtop")
        opts = ["Q","R","B","N"]
        bw2 = 56
        total = bw2*4 + 12*3
        bx_start = px + (pw - total)//2
        self.promo_buttons = []
        for i, t in enumerate(opts):
            p = t if self.gs.turn == "W" else t.lower()
            bx3 = bx_start + i*(bw2+12)
            btn = Button((bx3, py+55, bw2, bw2), sym(p), font=F_BIG,
                          color=C["btn"], hover_color=C["btn_hover"])
            btn.draw(surf)
            self.promo_buttons.append((btn, t))

    def _draw_status(self, surf):
        ow = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
        ow.fill((0, 0, 0, 180))
        surf.blit(ow, (0, 0))
        bw2, bh = 340, 160
        bx2 = (self.sw - bw2)//2
        by2 = (self.sh - bh)//2
        draw_rect(surf, C["panel"], (bx2, by2, bw2, bh), 14, 2, C["gold"])
        gs = self.gs
        if gs.winner:
            name = T("white") if gs.winner=="W" else T("black")
            draw_text(surf, T("winner", name), F_BIG, C["gold2"], self.sw//2, by2+30, "midtop")
        else:
            draw_text(surf, T("draw"), F_BIG, C["text2"], self.sw//2, by2+30, "midtop")
        btn = Button((self.sw//2-80, by2+90, 160, 40), T("new_game"),
                      color=C["accent2"], hover_color=C["accent"])
        btn.draw(surf)
        self._gameover_btn = btn

    def _draw_msg(self, surf, msg, color):
        s = F_SM.render(msg, True, color)
        r = s.get_rect(midtop=(self.sx + self.sw2//2, self.sy + 275))
        draw_rect(surf, (*color, 30), r.inflate(16, 8), 6)
        surf.blit(s, r)

    def handle(self, event):
        gs = self.gs

        # Promo overlay
        if gs.promo_at:
            for btn, t in self.promo_buttons:
                if btn.handle(event):
                    gs.promote(t)
                if event.type == pygame.MOUSEMOTION:
                    btn.hovered = btn.rect.collidepoint(event.pos)
            return

        # Game over overlay
        if gs.over:
            if hasattr(self, "_gameover_btn"):
                if self._gameover_btn.handle(event):
                    self.new_game()
                if event.type == pygame.MOUSEMOTION:
                    self._gameover_btn.hovered = self._gameover_btn.rect.collidepoint(event.pos)
            return

        # Board click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            rc = self.board_r.click_to_rc(*event.pos)
            if rc:
                r, c = rc
                if gs.sel:
                    mv = next((m for m in gs.legal if m[0]==r and m[1]==c), None)
                    if mv:
                        fr2, fc2 = gs.sel
                        gs.sel = None; gs.legal = []
                        gs.execute_move(fr2, fc2, *mv)
                        return
                    gs.sel = None; gs.legal = []
                if gs.can_select(r, c):
                    gs.sel = (r, c)
                    gs.legal = legal_moves_for(gs.board, r, c, gs.ep, gs.castling, gs.turn)
                return

        # Sidebar buttons
        if self.btn_roll.handle(event):
            d1, d2 = gs.roll()
            if d1:
                self.dice_vals = (d1, d2)
        if self.btn_end.handle(event):
            gs.end_turn()
        if self.btn_new.handle(event):
            self.new_game()

        # Resurrect buttons
        for btn, t in self.res_buttons:
            if btn.handle(event):
                gs.resurrect(t)
            if event.type == pygame.MOUSEMOTION:
                btn.hovered = btn.rect.collidepoint(event.pos)

        for btn in [self.btn_roll, self.btn_end, self.btn_new]:
            if event.type == pygame.MOUSEMOTION:
                btn.hovered = btn.rect.collidepoint(event.pos)

    def refresh_labels(self):
        self.btn_roll.label = T("roll_dice")
        self.btn_end.label  = T("end_turn")
        self.btn_new.label  = T("new_game")


# ─────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────
class App:
    def __init__(self):
        self.W, self.H = 920, 640
        self.screen = pygame.display.set_mode((self.W, self.H), pygame.RESIZABLE)
        pygame.display.set_caption(T("title"))
        self.clock = pygame.time.Clock()
        load_fonts()

        self.tab = "game"
        self.tabs = ["game", "settings", "learn"]
        self.tab_labels = {
            "game":     lambda: T("tab_game"),
            "settings": lambda: T("tab_settings"),
            "learn":    lambda: T("tab_learn"),
        }
        self.TAB_H = 44

        self.game_screen     = GameScreen(self.W, self.H - self.TAB_H)
        self.settings_screen = SettingsScreen(self.W, self.H - self.TAB_H)
        self.tutorial_screen = TutorialScreen(self.W, self.H - self.TAB_H)

        # Language toggle button
        self.btn_lang = Button((self.W - 110, 6, 100, 32), "EN / РУ", font=F_SM,
                                color=C["bg3"], hover_color=C["btn_hover"])

    def draw_tabs(self):
        surf = self.screen
        tab_w = (self.W - 120) // len(self.tabs)
        for i, t in enumerate(self.tabs):
            tx = 10 + i * (tab_w + 4)
            ty = 6
            is_active = t == self.tab
            bg = C["tab_active"] if is_active else C["bg3"]
            draw_rect(surf, bg, (tx, ty, tab_w, self.TAB_H - 10), 8,
                      1 if is_active else 0, C["border"])
            draw_text(surf, self.tab_labels[t](), F_MED, C["text"] if is_active else C["text2"],
                      tx + tab_w//2, ty + (self.TAB_H-10)//2, "center")

        # Separator line
        pygame.draw.line(surf, C["border"], (0, self.TAB_H), (self.W, self.TAB_H), 1)

    def handle_tabs(self, event):
        tab_w = (self.W - 120) // len(self.tabs)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if y < self.TAB_H:
                for i, t in enumerate(self.tabs):
                    tx = 10 + i * (tab_w + 4)
                    if tx <= x <= tx + tab_w:
                        self.tab = t
                        break

    def run(self):
        global LANG
        running = True
        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.VIDEORESIZE:
                    self.W, self.H = event.w, event.h
                    self.screen = pygame.display.set_mode((self.W, self.H), pygame.RESIZABLE)
                    self._rebuild()

                self.handle_tabs(event)

                if self.btn_lang.handle(event):
                    LANG = "en" if LANG == "ru" else "ru"
                    pygame.display.set_caption(T("title"))
                    self._refresh_labels()

                if event.type == pygame.MOUSEMOTION:
                    self.btn_lang.hovered = self.btn_lang.rect.collidepoint(event.pos)

                # Offset events for sub-screens
                if self.tab == "game":
                    # offset y by TAB_H
                    ev = self._offset_event(event, 0, -self.TAB_H)
                    self.game_screen.handle(ev)
                elif self.tab == "settings":
                    ev = self._offset_event(event, 0, -self.TAB_H)
                    result = self.settings_screen.handle(ev)
                elif self.tab == "learn":
                    ev = self._offset_event(event, 0, -self.TAB_H)
                    result = self.tutorial_screen.handle(ev)
                    if result == "exit":
                        self.tab = "game"

            # Draw
            self.screen.fill(C["bg"])
            self.draw_tabs()
            self.btn_lang.rect.topleft = (self.W - 110, 6)
            self.btn_lang.draw(self.screen)

            # Draw active sub-screen on offset surface
            sub_surf = pygame.Surface((self.W, self.H - self.TAB_H))
            if self.tab == "game":
                self.game_screen.sw = self.W
                self.game_screen.sh = self.H - self.TAB_H
                self.game_screen.draw(sub_surf)
            elif self.tab == "settings":
                self.settings_screen.sw = self.W
                self.settings_screen.sh = self.H - self.TAB_H
                self.settings_screen.draw(sub_surf)
            elif self.tab == "learn":
                self.tutorial_screen.sw = self.W
                self.tutorial_screen.sh = self.H - self.TAB_H
                self.tutorial_screen.draw(sub_surf)

            self.screen.blit(sub_surf, (0, self.TAB_H))
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def _offset_event(self, event, dx, dy):
        """Create a copy of event with mouse position offset"""
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            new_event = pygame.event.Event(event.type, dict(event.__dict__))
            if hasattr(new_event, 'pos'):
                new_event.pos = (new_event.pos[0] + dx, new_event.pos[1] + dy)
            return new_event
        return event

    def _rebuild(self):
        self.game_screen     = GameScreen(self.W, self.H - self.TAB_H)
        self.settings_screen = SettingsScreen(self.W, self.H - self.TAB_H)
        self.tutorial_screen = TutorialScreen(self.W, self.H - self.TAB_H)
        self.btn_lang = Button((self.W - 110, 6, 100, 32), "EN / РУ", font=F_SM,
                                color=C["bg3"], hover_color=C["btn_hover"])

    def _refresh_labels(self):
        pygame.display.set_caption(T("title"))
        self.game_screen.refresh_labels()
        self.settings_screen.refresh_labels()
        self.tutorial_screen.refresh_labels()


if __name__ == "__main__":
    App().run()
