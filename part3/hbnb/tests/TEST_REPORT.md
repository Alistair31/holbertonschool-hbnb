Module,Test Case,Expected,Actual,Status

Amenities
,test_create_amenity,201,201,PASS ✅
,test_create_invalid_amenity,400,400,PASS ✅
,test_get_all_amenities,200,200,PASS ✅
,test_update_amenity,200,200,PASS ✅

Reviews
,test_create_review_flow,201/200,201/200,PASS ✅
,test_create_review_invalid_rating,400,400,PASS ✅
,test_create_review_missing_data,400,400,PASS ✅
,test_get_non_existent_review,404,404,PASS ✅

Users
,test_create_user_success,201,201,PASS ✅
,test_create_user_duplicate_email,400,400,PASS ✅
,test_create_user_missing_fields,400,400,PASS ✅
,test_get_user_by_id,200,200,PASS ✅
,test_update_user,200,200,PASS ✅
,test_get_non_existent_user,404,404,PASS ✅

Places
,test_place_amenities_relation,201,201,PASS ✅
,test_place_immutability_and_validation,200,200,PASS ✅
,test_place_invalid_coordinates,400,400,PASS ✅
,test_place_update_invalid_price,400,400,PASS ✅
,test_get_non_existent_place,404,404,PASS ✅
,test_update_non_existent_place,404,404,PASS ✅
