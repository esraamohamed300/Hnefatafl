from GUI.window import GameWindow

if __name__ == "__main__":
    game = GameWindow()
    game.run()
    # test_ai.py - اختبار مستقل للـ AI
print("🧪 اختبار Alpha-Beta + Evaluation...")

# استيراد الملفات
from game_state import GameState
from alphabeta import alphabeta
from evaluation import Evaluation
from ai_player import AIPlayer

print("✅ Imports شغالة!")

# إنشاء board تجريبي
state = GameState()
print("✅ GameState شغال!")
print("Initial board:")
state.print_board()

# اختبار 1: Evaluation
eval_obj = Evaluation()
score = eval_obj.evaluate(state)
print(f"🏆 Initial evaluation: {score:.1f}")

# اختبار 2: Alpha-Beta
print("\n🤖 اختبار Alpha-Beta (depth=2)...")
moves = state.get_legal_moves("black")
if moves:
    best_move = AIPlayer("easy").get_move(state, "black")
    print(f"✅ أحسن move: {best_move}")
else:
    print("❌ No moves!")

print("\n🎉 الكل شغال! الـ AI جاهز!")
