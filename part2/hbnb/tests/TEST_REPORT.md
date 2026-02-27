Test reviews Case,Method,Description,Expected,Actual,Status

test_create_review_flow,POST/GET/PUT/DELETE,"Full lifecycle: Create, Retrieve, Update, and Delete a review.",201/200,201/200,PASS ✅
test_create_review_invalid_rating,POST,Negative test: Submit a rating of 10 (valid range is 1-5).,400,400,PASS ✅
test_create_review_missing_data,POST,Negative test: Submit review without required fields (text/place_id).,400,400,PASS ✅
test_get_non_existent_review,GET,Retrieve a review using a non-existent ID.,404,404,PASS ✅


Module,Total Tests,Status,Key Validations
Reviews,4,PASS ✅,"CRUD flow, Rating limits (1-5), Missing fields, 404 handling."
Amenities,4,PASS ✅,"Valid creation, Empty name rejection, Update messages, List retrieval."