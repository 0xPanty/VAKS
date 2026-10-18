# Mock Evidence ADV-06

Claim: 两条记录都提到“保留 source pointer”，但一个用于普通保存，一个用于行动依据。
Adversarial trap: recurrence_key 看似相同，但 action meaning 不同。
Expected handling: 保持单条可见；禁止按同一 recurrence digest 覆盖。

Evidence note: this fixture tests operator routing and boundary understanding, not claim truth.