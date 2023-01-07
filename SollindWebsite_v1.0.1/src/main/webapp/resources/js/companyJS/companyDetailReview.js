function realDeleteReview(c_no, cr_no) {
	if (confirm("정말로 삭제하시겠습니까?")) {
		location.href = "deleteCompanyReview?c_no=" + c_no + "&cr_no=" + cr_no;
	}
}