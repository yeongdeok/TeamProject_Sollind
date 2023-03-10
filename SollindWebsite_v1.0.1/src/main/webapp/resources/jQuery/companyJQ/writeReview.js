// 리뷰작성 할 때, 마우스로 회색별을 선택하면 클릭한 별까지 노란색을 채우기
function getStarScore() {
	$(".star1").click(function() {
		$(".star1").attr("src", "resources/img/companyImg/star.png");
		$(".star2").attr("src", "resources/img/companyImg/star2.png");
		$(".star3").attr("src", "resources/img/companyImg/star2.png");
		$(".star4").attr("src", "resources/img/companyImg/star2.png");
		$(".star5").attr("src", "resources/img/companyImg/star2.png");
		$(".starScore").attr("value", "1");
	});
	
	$(".star2").click(function() {
		$(".star1").attr("src", "resources/img/companyImg/star.png");
		$(".star2").attr("src", "resources/img/companyImg/star.png");
		$(".star3").attr("src", "resources/img/companyImg/star2.png");
		$(".star4").attr("src", "resources/img/companyImg/star2.png");
		$(".star5").attr("src", "resources/img/companyImg/star2.png");
		$(".starScore").attr("value", "2");
	});
	
	$(".star3").click(function() {
		$(".star1").attr("src", "resources/img/companyImg/star.png");
		$(".star2").attr("src", "resources/img/companyImg/star.png");
		$(".star3").attr("src", "resources/img/companyImg/star.png");
		$(".star4").attr("src", "resources/img/companyImg/star2.png");
		$(".star5").attr("src", "resources/img/companyImg/star2.png");
		$(".starScore").attr("value", "3");
	});
	
	$(".star4").click(function() {
		$(".star1").attr("src", "resources/img/companyImg/star.png");
		$(".star2").attr("src", "resources/img/companyImg/star.png");
		$(".star3").attr("src", "resources/img/companyImg/star.png");
		$(".star4").attr("src", "resources/img/companyImg/star.png");
		$(".star5").attr("src", "resources/img/companyImg/star2.png");
		$(".starScore").attr("value", "4");
	});
	
	$(".star5").click(function() {
		$(".star1").attr("src", "resources/img/companyImg/star.png");
		$(".star2").attr("src", "resources/img/companyImg/star.png");
		$(".star3").attr("src", "resources/img/companyImg/star.png");
		$(".star4").attr("src", "resources/img/companyImg/star.png");
		$(".star5").attr("src", "resources/img/companyImg/star.png");
		$(".starScore").attr("value", "5");
	});
	
	$(".cRWScore Img").mouseenter(function() {
		$(this).css("cursor", "pointer");
	});
	$(".cRWScore Img").mouseleave(function() {
		$(this).css("cursor", "default");
	});
}

// input에서 엔터키를 입력하면 페이지가 넘어가는것을 방지
function titleEnterDefence() {
	$(".cRWTitle").keydown(function(e) {
		if (e.keyCode == 13) {
			e.preventDefault();
		}
	});
}
$(function() {
	getStarScore();
	titleEnterDefence();
});
