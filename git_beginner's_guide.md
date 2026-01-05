# 왕초보 Git/Github 사용법

## 초기 세팅은 지피티한테 물어보자

-   `git init`, `git clone` 등 초기 세팅은 가끔씩 해서 할때마다 헷갈리니까 지피티한테 물어보는 게 젤 맘편함.

## 개발은 `develop` 브랜치에서, 배포는 `main` 브랜치에서

-   처음부터 `main` 브랜치를 수정하면 버그가 났을 때 배포를 못할 수도 있으므로,
-   코드 수정은 `develop` 브랜치에서 하고, 수정이 완료된 뒤에 `develop` 브랜치를 `main` 브랜치로 `merge`한다.
-   `render.com`에서 배포할 때 사용할 브랜치로는 `main` 브랜치를 선택한다.

## 코드를 수정할 때는 무조건 아래의 순서를 따른다.

1. `git switch develop`
    - develop 브랜치로 이동한다.
2. `git pull`
    - 깃허브 상의 develop 브랜치의 내용을 내 로컬 컴퓨터의 develop 브랜치로 가져온다.
    - 다른 팀원이 develop 브랜치를 수정하지 않았다면 아무 변화가 없음
3. develop 브랜치에서 코드를 수정한다.
4. `git add .`
    - 수정/추가한 내용을 commit할 준비를 한다.
    - 코드를 수정한 뒤 아무것도 add 해놓지 않으면 commit이 안 된다.
    - 일부 파일만 add한 뒤에 commit하게 되면 나중에 골치아파지므로 되도록 수정한 모든 파일을 add 해놓자.
5. `git commit -m "커밋 제목" -m "커밋 세부설명"`
    - add된 모든 파일을 한 뭉텅이로 묶어서 commit한다. commit 이후에도 아직 깃허브에 반영된 것은 아니고 내 로컬 컴퓨터에만 한 단락이 저장됐다고 보면 된다.
    - 두번째 -m과 세부설명은 생략 가능한다.
    - 하나의 기능을 수정 후에 바로 commit을 해놓고 다음 기능을 수정하고 또 commit하자. 너무 많은 작업을 하나로 commit 해버리면 나중에 이때 무엇을 수정했는지 알기가 어렵다.
6. `git push origin develop`
    - commit된 코드들을 깃허브의 develop 브랜치에 반영한다. 내 로컬 컴퓨터에서 수정한 코드를 인터넷으로 올리는 것이라고 보면 된다.

---

7. `git switch main`
    - main branch로 이동한다.
8. `git merge develop`
    - develop 브랜치의 변경사항을 main 브랜치에 반영한다.
9. `git push origin main`
    - main 브랜치의 변경사항을 깃허브에 반영한다.

## 알아두면 편한 git 명령어들

-   `git branch` 브랜치 목록 보기 및 현재 브랜치 확인
-   `git switch <브랜치 이름>` 다른 브랜치로 이동하기
    -   [주의] `switch` 전에는 무조건 모든 변경사항을 `commit` 해놓고 가야 된다. 안 그러면 다른 브랜치의 파일들이 뒤섞임.
    -   아직 커밋할 준비가 안 됐다면, `git stash` 해놓고 다른 브랜치에 갔다가 돌아와서 `git stash pop`하면 원래 작업하던 상태로 돌아온다. 근데 까먹을 수 있어서 비추.
-   `git status` 현재 내가 위치해있는 브랜치에서 어떤 변경사항이 staged(add) 되어있는지 확인
-   `git add <파일 이름>` 특정한 파일만 stage시킴
-   `git add .` 현재 디렉토리의 모든 파일을 stage시킴

## 참고) `origin/main`과 `main`의 차이 (다른 브랜치들도 마찬가지)

-   `origin/main` -> 깃허브에 올라가있는 버전의 main이라는 이름의 브랜치
-   그냥 `main` -> 내 컴퓨터(로컬 환경)에 저장되어있는 버전의 main이라는 이름의 브랜치
