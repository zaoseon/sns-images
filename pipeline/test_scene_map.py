# 시험: python3 pipeline/test_scene_map.py
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene_map as m
ok_plan = [("용어·키워드", "키네틱 글자"), ("숫자·비율", "큰 숫자 세기"), ("비교", "좌우 비교 패널"), ("기능·결과 보여 주기", "실제 화면"), ("정리·마무리", "체크 목록")]
assert m.lint(ok_plan) == [], m.lint(ok_plan)
bad = m.lint([("숫자·비율", "막대"), ("숫자·비율", "막대"), ("기능·결과 보여 주기", "막대"), ("그외", "x")])
assert len(bad) == 4 and "연달아" in bad[0] and "맞지 않아요" in bad[1] and "모르는" in bad[3], bad
assert all(f for v in m.MAP.values() for f in v)
print("모두 통과")
