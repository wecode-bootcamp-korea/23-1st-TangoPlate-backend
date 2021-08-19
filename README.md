# 탱고 플레이트 (망고플레이트 클론코딩)

![Screen Shot 2021-08-19 at 5 19 22 PM](https://user-images.githubusercontent.com/8315252/130033730-65f628fc-9cfa-4167-a2a1-2de44e7be1d8.png)


## Tango Plate Project Family

- F.E<br>
  [이정일](https://github.com/201steve) : 인간 망고플레이트 / 해당 프로젝트에 진심인 개발자<br>
  [최정민](https://github.com/minmin9324) : F.E 막내 On top / F.E에서 실질적 PM의 위치<br>
  [김명성](https://github.com/sstaar91/) : 여얼쩡 여얼쩡 / 팀에서 말이 제일 많지만 분위기를 담당하고 있음<br>
  <br>
- B.E<br>
  [고유영](https://github.com/lunayyko) : 망고 플레이트 제안자 / 정신적 지주이자 우리들의 PM<br>
  [한승훈](https://github.com/Samdaso-o) : B.E 능력자 / 다른 조에서도 눈독 들이고 있는 B.E top class/ 존잘남<br> 
  <br>

## What is Tango Plate Project?

- 국내 맛집이란 맛집은 다 모인 [망고플레이트](https://www.mangoplate.com/) 클론 프로젝트
- 촉박한 프로젝트 기간으로 최소 기능을 구현할 수 있는 페이지만 클론
- wecode Bootcamp에서 배운 내용들을 바탕으로 구현할 수 있는 기능들과<br>
  그 외에 추가로 구현할 수 있는 기능들을 선정해 구현했습니다.
- 개발은 초기 세팅부터 직접 구현했으며, 프론트와 백을 연결해 실제 사용 가능한 수준으로 개발했습니다.

### 개발 인원 및 기간

- 개발기간 : 2021/8/2 ~ 2021/8/13
- 개발 인원 : 프론트엔드 3명, 백엔드 2명
- [F.E github 링크](https://github.com/wecode-bootcamp-korea/23-1st-TangoPlate-frontend)

### 프로젝트 선정이유

- 그동안 wecode에서 구현했던 기술들을 접목해 클론 하기 적합한 난이도
- 사용자에게 일방적인 정보 제공보다 여러 사용자의 데이터를 기반으로<br>다른 사용자에게 나은 정보를 제공한다는 점에 매력을 느낌
- 인간의 3대욕구 중 하나와 관련된 사이트이다 보니, 코드로 구현하는 부분 외에도<br>다양한 즐거운 부분이 있어 프로젝트 진행 과정에서 지치지 않고 할 수 있음

## 적용 기술 및 구현 기능

### 적용 기술

> -Front-End : javascript, React.js framwork, sass<br>
> -Back-End : Python, Django web framework, MySQL, Bcrypt, pyjwt<br>
> -Common : POSTMAN, RESTful API

### 구현 기능

#### 회원가입 / 로그인페이지

- 회원가입 시 정규식을 통한 유효성 검사. (소문자, 대문자, 특수문자의 조합)
- 로그인을 이후 토큰 발행, 계정 활성화
- 계정 없을 시 바로 회원가입으로 이동할 수 있도록 구현.

#### 메인페이지

- 검색바에서 키워드 검색시 검색결과 상단에 검색값 + 맛집 리스트 페이지로 이동.
- 우측 상당 맛집 리스트 클릭시 상단에 필터리스트 + 맛집 리스트 페이지로 이동.
- 잇딜 클릭시 잇딜 리스트 페이지로 이동 (추가 구현)
- 하단 푸터를 통한 사이트 설명.

#### 검색 페이지

- 키워드(카테고리, 지역, 가격대별) 필터
- 메뉴, 주소, 카테고리, 식당 이름 등으로 검색
- 페이지네이션

#### 맛집 리스트 페이지

- 카테고리에 대한 식당 리스트를 평점순으로 나열.
- 클릭시 상세 페이지로 이동.

#### 상세페이지

- 해당 식당의 사진들, 상세정보, 별점, 가고싶다 여부.
- 식당에 대한 리뷰 평점순으로 나열, 페이지네이션.
- 가고싶다(위시리스트) 생성, 삭제
- 리뷰 생성, 수정, 삭제
- 네비게이션 바
- 검색바.
- 회원가입, 로그인 버튼.
- 이름, 가고싶다 목록 등 유저 정보.

<br>

## Reference

- 이 프로젝트는 [망고플레이트](https://www.mangoplate.com/) 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.
