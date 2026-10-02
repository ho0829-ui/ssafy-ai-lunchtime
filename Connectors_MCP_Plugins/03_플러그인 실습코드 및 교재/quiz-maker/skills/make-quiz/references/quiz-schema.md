# quiz.json 스키마

```json
{
  "title": "파이썬 리스트 기초 확인 퀴즈",
  "source_files": ["03_리스트.md"],
  "instructions": "객관식은 가장 알맞은 것 하나를 고르시오.",
  "questions": [
    {
      "id": 1,
      "type": "mc",
      "stem": "다음 중 리스트의 특징으로 옳은 것은?",
      "choices": ["원소를 수정할 수 없다", "순서가 없다", "서로 다른 자료형을 함께 담을 수 있다", "중복 원소를 허용하지 않는다"],
      "answer": 3,
      "explanation": "리스트는 이종 자료형을 담을 수 있다. ①은 튜플, ②④는 집합의 특징이다.",
      "evidence": [
        {"pid": "P4", "quote": "리스트는 서로 다른 자료형의 값을 함께 담을 수 있다."}
      ]
    },
    {
      "id": 2,
      "type": "short",
      "stem": "리스트 끝에 원소 하나를 추가하는 메서드 이름을 쓰시오.",
      "code": "nums = [1, 2]\nnums.____(3)",
      "code_lang": "python",
      "answer": "append",
      "accept": ["append()", ".append"],
      "explanation": "append는 원소 하나를 리스트 끝에 추가한다.",
      "evidence": [
        {"pid": "P9", "quote": "append() 메서드는 리스트의 맨 끝에 원소 하나를 추가한다."}
      ]
    }
  ]
}
```

## 필드

| 필드 | 필수 | 설명 |
|---|---|---|
| `title` | ○ | 파일명에도 쓰임 (`<title>_문제지.md`) |
| `source_files` | | 출제 범위 표기. 생략 시 색인의 파일명 사용 |
| `instructions` | | 문제지 상단 안내 문구 |
| `id` | ○ | 1부터 연속 정수 |
| `type` | ○ | `mc`(객관식) / `short`(단답형) |
| `stem` | ○ | 문제 본문. 첫 줄은 정답지 소제목으로도 쓰임 |
| `code`, `code_lang` | | 문제에 딸린 코드 블록 |
| `choices` | mc | 4~5개, 중복 불가 |
| `answer` | ○ | mc: 1부터 시작하는 번호 / short: 대표 정답 문자열 |
| `accept` | | short 전용, 추가 인정 답안 |
| `explanation` | 권장 | 정답 이유 + (객관식) 주요 오답이 틀린 이유 |
| `evidence[].pid` | ○ | `source_numbered.md`의 `[P#]` 번호 |
| `evidence[].quote` | ○ | 해당 문단 원문을 글자 그대로 복사한 연속 구간 (5자 이상) |

## 검증 규칙 (build_quiz.py)
- 오류(파일 미생성): id 불연속, type 오류, 선택지 수·중복, answer 범위, 근거 누락, 없는 pid, **인용-원문 불일치**(공백·따옴표 모양 차이만 허용).
- 경고: 객관식 정답이 한 번호에 40% 초과 집중, "모두 정답/정답 없음"류 선택지, 단답형 정답이 본문에 노출.
