- onMouseButton
rollercoaster 재생동안은 마우스 클릭이 안되게  key_lock 변수를 통해 제어했습니다
GLFW_DOWN -> isDrag 가 V_DRAG 로 변합니다.
GLFW_UP -> isDrag 가 0이 아닐때 cowCtrlSz가 0이 아닌지 확인(첫번째 상자를 클릭하는 것을 제외)후 현재 cow2wld를 cowCtrlP에 저장.
cowCtrlSz 1증가

- onMouseDrag
마우스 선택시에도 계속 pickInfo 에 현재 상태 저장.
드래그시 현재 카메라 벡터를 xy평면에 정사영한 벡터를 평면의 normal 벡터로 같은 평면을 만들고 그 평면과의 교점의 수직방향 벡터 계산.

- display
6개가 선택이 되면 qk-1, qk0, qk1, qk2 을 미리 입력해놓은 catmull rom 배열과 곱한다.
나온값을 하나는 t^3, t^2, t^1, 1과 곱하여 curve 위치를 찾고 translation한다.
하나는 미분하여 벡터를 구하는데, 3*t^2, 2*t^1, 1, 0 를 곱하여 얻는다.
그다음 math.atan2를 이용하여 각각 수평 수직 각도를 구한 후 각각 y, x축을 기준으로 rotation 한다.

