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
        self.turn = opp(self.turn)
        self.rolled = False; self.act_used = 0; self.moved_pieces = {}
        self.crit = False; self.crit_key = None; self.crit_used = False
        self.od[self.turn] = 0
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
    glyph = PIECE_GLYPH[t]
    is_w = is_white(piece_char)
    fill = C["piece_w"] if is_w else C["piece_b"]
    outline = C["piece_w_outline"] if is_w else C["piece_b_outline"]

    if size not in _symbol_font_cache:
        sfp = get_symbol_font_path()
        if sfp:
            _symbol_font_cache[size] = pygame.font.Font(sfp, size)
        else:
            _symbol_font_cache[size] = pygame.font.SysFont("segoeuisymbol,dejavusans", size)
    font = _symbol_font_cache[size]

    surf = pygame.Surface((size + 8, size + 8), pygame.SRCALPHA)
    outline_surf = font.render(glyph, True, outline)
    fill_surf = font.render(glyph, True, fill)
    pad = 2
    for dx in range(-pad, pad + 1):
        for dy in range(-pad, pad + 1):
            if dx == 0 and dy == 0: continue
            surf.blit(outline_surf, (4 + dx, 4 + dy))
    surf.blit(fill_surf, (4, 4))
    _piece_cache[key] = surf
    return surf

def clear_piece_cache():
    _piece_cache.clear()
    _symbol_font_cache.clear()


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
        bw = max(28, self.rect.height)
        self.btn_minus = pygame.Rect(self.rect.x, self.rect.y, bw, self.rect.height)
        self.btn_plus  = pygame.Rect(self.rect.right - bw, self.rect.y, bw, self.rect.height)
        self.val_rect  = pygame.Rect(self.rect.x + bw, self.rect.y,
                                     self.rect.width - 2*bw, self.rect.height)

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
    elif fail:
        bg = C["die_fail"]; border = (200,80,80)
    elif player_color == "W":
        bg = (55, 55, 70); border = (200, 200, 220)
    elif player_color == "B":
        bg = (25, 25, 35); border = (80, 80, 100)
    else:
        bg = C["die_bg"]; border = C["border2"]
    draw_rect(surf, bg, rect, 8, 2, border)
    if val < 1 or val > 6:
        draw_text(surf, "?", FONTS["med"], C["text2"], rect.centerx, rect.centery, "center")
        return
    dot_color = (220,240,200) if crit else (240,180,180) if fail else \
                (240,240,250) if player_color == "W" else \
                (180,180,200) if player_color == "B" else C["text"]
    r = max(3, rect.width // 10)
    for fx, fy in DIE_DOTS[val]:
        cx = int(rect.x + fx * rect.width)
        cy = int(rect.y + fy * rect.height)
        pygame.draw.circle(surf, dot_color, (cx, cy), r)


class SettingsScreen:
    def __init__(self):
        self.scroll_y = 0
        self.content_h = 0
        self.spinners_piece = {}
        self.spinners_global = {}
        self.locked = False   # True during active game
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
        margin = 30
        max_w = min(880, w - 2 * margin)
        x_start = (w - max_w) // 2

        col_label = 130
        col_w = (max_w - col_label) // 3
        spinner_w = min(120, col_w - 24)

        self._x_label = x_start + 8
        self._spinner_w = spinner_w
        self._col_centers = [
            x_start + col_label + col_w // 2,
            x_start + col_label + col_w + col_w // 2,
            x_start + col_label + 2 * col_w + col_w // 2,
        ]
        self._x_start = x_start
        self._max_w = max_w

        y = 24
        self._title_y = y
        y += 50
        self._piece_header_y = y
        # Header now takes 50px (title + 2 hint lines)
        y += 50
        row_h = 44

        for i, t in enumerate(PIECE_TYPES):
            ry = y + i * row_h
            for j, key_kind in enumerate(["move", "res_cost", "res_count"]):
                cx = self._col_centers[j]
                self.spinners_piece[(key_kind, t)].set_rect(
                    (cx - spinner_w // 2, ry, spinner_w, 32))
        y += len(PIECE_TYPES) * row_h + 24
        self._sep_y = y
        y += 18
        self._global_header_y = y
        y += 32

        x_global_label = x_start + 16
        x_global_spin = x_start + max_w - spinner_w - 16
        # Global rows are taller (label + hint)
        global_row_h = 54
        for i, k in enumerate(["max_actions","crit_ap","fail_penalty","castle_cost"]):
            ry = y + i * global_row_h
            self.spinners_global[k].set_rect((x_global_spin, ry + 18, spinner_w, 32))
        self._x_global_label = x_global_label
        y += 4 * global_row_h + 12

        # En passant toggle row
        self._ep_y = y
        self._ep_toggle_x = x_global_spin + spinner_w - self.ep_toggle.w
        self.ep_toggle.set_pos(self._ep_toggle_x, y + 2)
        y += global_row_h + 10

        btn_w = 160; btn_gap = 16
        total = 2 * btn_w + btn_gap
        bx = (w - total) // 2
        self.btn_save.rect = pygame.Rect(bx, y, btn_w, 40)
        self.btn_reset.rect = pygame.Rect(bx + btn_w + btn_gap, y, btn_w, 40)
        y += 60
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
            hint_lines = wrap_text(T(hint_key), FONTS["xs"], self._spinner_w + 30)
            for j, line in enumerate(hint_lines[:2]):
                draw_text(content, line, FONTS["xs"], C["text3"],
                          self._col_centers[i], self._piece_header_y + 20 + j * 14, "midtop")

        row_h = 44
        for i, t in enumerate(PIECE_TYPES):
            ry = self._piece_header_y + 50 + i * row_h
            draw_text(content, TP(t), FONTS["med"], C["text"],
                      self._x_label, ry + 16, "midleft")
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
            row_top = sp.rect.top - 18
            draw_text(content, lbl, FONTS["med"], C["text"],
                      self._x_global_label, row_top + 2, "topleft")
            draw_text(content, T(hint_key), FONTS["xs"], C["text3"],
                      self._x_global_label, row_top + 20, "topleft")
            sp.draw(content)

        # En passant toggle
        ep_lbl_col = C["text3"] if self.locked else C["text"]
        draw_text(content, T("allow_ep"), FONTS["med"], ep_lbl_col,
                  self._x_global_label, self._ep_y + 2, "topleft")
        draw_text(content, T("hint_ep"), FONTS["xs"], C["text3"],
                  self._x_global_label, self._ep_y + 20, "topleft")
        self.ep_toggle.disabled = self.locked
        self.ep_toggle.draw(content)

        # Save/Reset — disable when locked
        self.btn_save.disabled = self.locked
        self.btn_reset.disabled = self.locked
        self.btn_save.draw(content)
        self.btn_reset.draw(content)

        surf.fill(C["bg"])
        surf.blit(content, (0, -self.scroll_y))

        # Locked banner (drawn on top of surf, not content)
        if self.locked:
            banner_h = 52
            pygame.draw.rect(surf, (40, 25, 10), (0, 0, surf.get_width(), banner_h))
            pygame.draw.line(surf, (140, 90, 20), (0, banner_h), (surf.get_width(), banner_h), 2)
            lock_icon = "🔒 " if False else "⚠  "  # just use text
            draw_text(surf, T("settings_locked"), FONTS["med"], (220, 160, 50),
                      surf.get_width() // 2, 10, "midtop")
            draw_text(surf, T("settings_lock_hint"), FONTS["sm"], (160, 120, 40),
                      surf.get_width() // 2, 30, "midtop")

        # Scrollbar
        if self.content_h > surf.get_height():
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
            self._apply(); return "saved"
        if self.btn_reset.clicked(ev):
            self._reset(); return "reset"
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

    def draw(self, surf):
        sw, sh = surf.get_width(), surf.get_height()
        surf.fill(C["bg"])
        steps = get_tutorial_steps()
        total = len(steps)
        self.step = max(0, min(self.step, total - 1))
        title, body = steps[self.step]

        bar_x, bar_y = 60, 50
        bar_w = sw - 120
        pygame.draw.rect(surf, C["bg3"], (bar_x, bar_y, bar_w, 6), border_radius=3)
        prog = int(bar_w * (self.step + 1) / total)
        pygame.draw.rect(surf, C["accent"], (bar_x, bar_y, prog, 6), border_radius=3)
        draw_text(surf, f"{self.step+1} / {total}", FONTS["sm"], C["text3"],
                  sw // 2, bar_y - 18, "center")

        card_x = 60; card_y = 80
        card_w = sw - 120; card_h = sh - 180
        draw_rect(surf, C["panel"], (card_x, card_y, card_w, card_h), 12, 1, C["border"])

        draw_text(surf, title, FONTS["big"], C["gold2"],
                  sw // 2, card_y + 28, "midtop")
        pygame.draw.line(surf, C["border"],
                         (card_x + 30, card_y + 70),
                         (card_x + card_w - 30, card_y + 70), 1)

        text_x = card_x + 40
        text_y = card_y + 90
        max_w = card_w - 80
        lines = wrap_text(body, FONTS["med"], max_w)
        for i, line in enumerate(lines):
            ly = text_y + i * (FONTS["med"].get_height() + 5)
            if ly > card_y + card_h - 30: break
            draw_text(surf, line, FONTS["med"], C["text"], text_x, ly)

        bw = 160; gap = 16
        ty = sh - 60
        cx = sw // 2
        self.btn_prev.rect = pygame.Rect(cx - bw - gap // 2, ty, bw, 40)
        self.btn_next.rect = pygame.Rect(cx + gap // 2, ty, bw, 40)
        self.btn_exit.rect = pygame.Rect(sw - 160, ty, 140, 40)

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

    def new_game(self):
        self.gs = GameState()
        self.gs.add_log(T("log_newgame"), "sys")
        self.dice_vals = (0, 0)

    def _layout(self, w, h):
        side_w = 280
        margin = 16
        avail_w = w - side_w - 3 * margin
        avail_h = h - 2 * margin
        self.bsize = min(avail_w, avail_h)
        self.bsize = (self.bsize // 8) * 8
        if self.bsize < 240: self.bsize = 240
        self.sq = self.bsize // 8
        self.bx = margin + (avail_w - self.bsize) // 2
        self.by = margin + (avail_h - self.bsize) // 2

        self.sx = self.bx + self.bsize + margin
        self.sy = margin
        self.sw_panel = w - self.sx - margin

        bx2 = self.sx + 10
        bw = self.sw_panel - 20
        self.btn_roll.rect = pygame.Rect(bx2, self.sy + 130, bw, 38)
        self.btn_end.rect  = pygame.Rect(bx2, self.sy + 174, bw, 38)
        self.btn_new.rect  = pygame.Rect(bx2, h - 50, bw, 36)

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
        self._draw_board(surf)
        self._draw_sidebar(surf)
        if self.gs.promo_at:
            self._draw_promo(surf)
        elif self.gs.over:
            self._draw_status_overlay(surf)

    def _draw_board(self, surf):
        gs = self.gs
        for r in range(8):
            for c in range(8):
                light = (r + c) % 2 == 0
                rect = pygame.Rect(self.bx + c * self.sq, self.by + r * self.sq, self.sq, self.sq)
                if gs.check_sq and (r, c) == gs.check_sq: col_sq = C["sq_check"]
                elif gs.sel and (r, c) == gs.sel: col_sq = C["sq_sel"]
                elif gs.legal and any(tr == r and tc == c for tr, tc, _ in gs.legal):
                    col_sq = C["sq_cap"] if gs.board[r][c] else C["sq_can"]
                else:
                    col_sq = C["sq_light"] if light else C["sq_dark"]
                pygame.draw.rect(surf, col_sq, rect)
                if r == 7:
                    draw_text(surf, f2l(c), FONTS["coord"],
                              C["text3"] if light else C["sq_light"],
                              rect.right - 3, rect.bottom - 2, "bottomright")
                if c == 0:
                    draw_text(surf, str(8 - r), FONTS["coord"],
                              C["text3"] if light else C["sq_light"],
                              rect.left + 2, rect.top + 1)
                p = gs.board[r][c]
                if p:
                    psize = int(self.sq * 0.78)
                    surf_p = piece_surface(p, psize)
                    pr = surf_p.get_rect(center=rect.center)
                    surf.blit(surf_p, pr)
        pygame.draw.rect(surf, C["border2"],
                         (self.bx-1, self.by-1, self.bsize+2, self.bsize+2),
                         2, border_radius=4)

    def _draw_sidebar(self, surf):
        gs = self.gs
        sx = self.sx; sy = self.sy; sw = self.sw_panel
        bx2 = sx + 10
        sh = surf.get_height()

        for i, color in enumerate(["W","B"]):
            py = sy + i * 58
            is_active = gs.turn == color and not gs.over
            bg = C["panel2"] if is_active else C["panel"]
            border = C["accent"] if is_active else C["border"]
            draw_rect(surf, bg, (sx, py, sw, 52), 8, 2, border)

            name = T("white") if color == "W" else T("black")
            psurf = piece_surface(("K" if color == "W" else "k"), 22)
            surf.blit(psurf, (bx2 - 4, py + 6))
            draw_text(surf, name, FONTS["med"], C["text"], bx2 + 28, py + 14)

            od_val = gs.od[color]
            od_str = f"{od_val} {T('ap_label')}"
            draw_text(surf, od_str, FONTS["big"],
                      C["gold2"] if is_active else C["text2"],
                      sx + sw - 10, py + 10, "topright")

            bar_w = sw - 20
            draw_rect(surf, C["bg3"], (bx2, py + 40, bar_w, 6), 3)
            fill_w = int(bar_w * min(1.0, od_val / 12))
            fill_c = C["red2"] if od_val <= 2 and gs.rolled else C["accent"]
            if fill_w > 0:
                draw_rect(surf, fill_c, (bx2, py + 40, fill_w, 6), 3)

        phase_lbl = {"normal": T("phase_normal"), "gambit": T("phase_gambit"), "clash": T("phase_clash")}.get(gs.phase, "")
        phase_col = C["gold2"] if gs.phase != "normal" else C["text2"]
        draw_text(surf, phase_lbl, FONTS["sm"], phase_col,
                  sx + sw // 2, sy + 118, "midtop")

        self.btn_roll.disabled = gs.rolled or gs.over
        self.btn_end.disabled = not gs.rolled or gs.over
        self.btn_roll.draw(surf)
        self.btn_end.draw(surf)

        dy = self.btn_end.rect.bottom + 16
        die_size = 42; gap = 12
        total_w = 2 * die_size + gap
        dx = sx + (sw - total_w) // 2
        d1, d2 = self.dice_vals
        crit = d1 + d2 == 12 and d1 > 0
        fail = d1 + d2 == 2 and d1 > 0
        pc_ = gs.turn if gs.rolled else None
        draw_die(surf, d1, pygame.Rect(dx, dy, die_size, die_size), crit, fail, pc_)
        draw_die(surf, d2, pygame.Rect(dx + die_size + gap, dy, die_size, die_size), crit, fail, pc_)

        acts_y = dy + die_size + 10
        if gs.rolled:
            acts_str = T("actions_label", gs.act_used, settings["max_actions"])
            if gs.crit and not gs.crit_used: acts_str += " ★"
            acts_col = C["gold2"] if gs.crit and not gs.crit_used else C["text2"]
        else:
            acts_str = T("roll_prompt"); acts_col = C["text2"]
        draw_text(surf, acts_str, FONTS["sm"], acts_col, sx + sw // 2, acts_y, "midtop")

        msg_y = acts_y + 24
        if not gs.over:
            if gs.check_sq:
                enemy = opp(gs.turn)
                en_name = T("white") if enemy == "W" else T("black")
                draw_text(surf, f"{T('check')} ({en_name})", FONTS["sm"],
                          C["red2"], sx + sw // 2, msg_y, "midtop")
                msg_y += 24
            if gs.phase == "gambit" and gs.rolled:
                draw_text(surf, T("phase_gambit"), FONTS["sm"], C["gold"],
                          sx + sw // 2, msg_y, "midtop")
                msg_y += 24
            if gs.phase == "clash" and gs.rolled:
                draw_text(surf, T("phase_clash"), FONTS["sm"], C["accent"],
                          sx + sw // 2, msg_y, "midtop")
                msg_y += 24

        self.res_buttons = []
        if gs.phase == "clash" and gs.rolled and not gs.over:
            res_items = gs.get_resurrectable()
            if res_items:
                draw_text(surf, T("resurrect"), FONTS["sm"], C["text2"], bx2, msg_y)
                msg_y += 22
                for t, cost in res_items:
                    label = f"{TP(t)} ({cost} {T('ap_label')})"
                    btn = Button((bx2, msg_y, sw - 20, 30), label,
                                  color=C["bg3"], hover_color=C["panel2"], font=FONTS["sm"])
                    btn.disabled = gs.act_used >= settings["max_actions"] or gs.od[gs.turn] < cost
                    btn.draw(surf)
                    self.res_buttons.append((btn, t))
                    msg_y += 34

        # Log positioned ABOVE the new game button — does not overlap
        log_bottom = self.btn_new.rect.top - 10
        log_top = max(msg_y + 10, log_bottom - 180)
        log_h = log_bottom - log_top
        if log_h > 50:
            draw_rect(surf, C["panel"], (sx, log_top, sw, log_h), 8, 1, C["border"])
            draw_text(surf, T("log_title"), FONTS["xs"], C["text3"], bx2, log_top + 6)
            line_y = log_top + 24
            for msg, mc in gs.log:
                if line_y + 18 > log_top + log_h - 6: break
                col_text = C["gold2"] if mc == "W" else C["text2"] if mc == "B" else C["text3"]
                s = msg
                while FONTS["xs"].size(s)[0] > sw - 24 and len(s) > 4:
                    s = s[:-1]
                if len(s) < len(msg): s = s[:-3] + "..."
                draw_text(surf, s, FONTS["xs"], col_text, bx2, line_y)
                line_y += 18

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
                        gs.promote(t); return
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
                        gs.sel = None; gs.legal = []
                        gs.execute_move(fr, fc, *mv)
                        return
                    gs.sel = None; gs.legal = []
                if gs.can_select(r, c):
                    gs.sel = (r, c)
                    gs.legal = legal_moves_for(gs.board, r, c, gs.ep, gs.castling, gs.turn)
                return

        if self.btn_roll.clicked(event):
            d1, d2 = gs.roll()
            if d1: self.dice_vals = (d1, d2)
        if self.btn_end.clicked(event):
            gs.end_turn()
        if self.btn_new.clicked(event):
            self.new_game()
        for btn, t in self.res_buttons:
            if btn.clicked(event):
                gs.resurrect(t)

    def refresh_labels(self):
        self.btn_roll.label = T("roll_dice")
        self.btn_end.label  = T("end_turn")
        self.btn_new.label  = T("new_game")


class App:
    def __init__(self):
        self.W, self.H = 1100, 700
        self.MIN_W, self.MIN_H = 900, 600
        self.screen = pygame.display.set_mode((self.W, self.H), pygame.RESIZABLE)
        pygame.display.set_caption("Chess of Evil")
        self.clock = pygame.time.Clock()

        load_fonts()
        clear_piece_cache()

        self.tab = "game"
        self.tabs = ["game", "settings", "learn"]
        self.tab_label_keys = {"game":"tab_game","settings":"tab_settings","learn":"tab_learn"}
        self.TAB_H = 44

        # Persistent screens — no recreation on resize
        self.game_screen = GameScreen()
        self.settings_screen = SettingsScreen()
        self.tutorial_screen = TutorialScreen()
        self.btn_lang = Button((0,0,90,32), "EN / РУ", font=FONTS["sm"],
                                color=C["bg3"], hover_color=C["btn_hover"])

    def draw_tabs(self):
        surf = self.screen
        self.btn_lang.rect = pygame.Rect(self.W - 100, 6, 90, 32)
        self.btn_lang.draw(surf)

        tabs_total_w = self.W - 110
        tab_w = (tabs_total_w - 8 * (len(self.tabs) - 1)) // len(self.tabs)
        for i, t in enumerate(self.tabs):
            tx = 10 + i * (tab_w + 8)
            ty = 8
            is_active = t == self.tab
            bg = C["tab_active"] if is_active else C["bg3"]
            draw_rect(surf, bg, (tx, ty, tab_w, self.TAB_H - 14), 8,
                      1 if is_active else 0, C["border"])
            draw_text(surf, T(self.tab_label_keys[t]), FONTS["med"],
                      C["text"] if is_active else C["text2"],
                      tx + tab_w // 2, ty + (self.TAB_H - 14) // 2, "center")
        pygame.draw.line(surf, C["border"], (0, self.TAB_H), (self.W, self.TAB_H), 1)

    def handle_tabs(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if y < self.TAB_H:
                tabs_total_w = self.W - 110
                tab_w = (tabs_total_w - 8 * (len(self.tabs) - 1)) // len(self.tabs)
                for i, t in enumerate(self.tabs):
                    tx = 10 + i * (tab_w + 8)
                    if tx <= x <= tx + tab_w:
                        self.tab = t; return True
        return False

    def run(self):
        global LANG
        running = True
        while running:
            self.clock.tick(60)
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

            self.screen.fill(C["bg"])
            self.draw_tabs()
            sub_w = self.W
            sub_h = self.H - self.TAB_H
            sub_surf = pygame.Surface((sub_w, sub_h))
            # Sync settings lock with game state
            self.settings_screen.locked = self.game_screen.gs.game_started and not self.game_screen.gs.over
            if self.tab == "game":
                self.game_screen.draw(sub_surf)
            elif self.tab == "settings":
                self.settings_screen.draw(sub_surf)
            elif self.tab == "learn":
                self.tutorial_screen.draw(sub_surf)
            self.screen.blit(sub_surf, (0, self.TAB_H))
            pygame.display.flip()

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
