import unittest

class ParkingTests(unittest.TestCase):
	def setUp(self):
		# connect api db to sqlite db
		# generate required classes via metadata
		pass

	def tearDown(self):
		# return api db to real db
		pass


	def test_retrieve_available(self):
		# insert into test db: 2 qvailable locs, 1 reserved locs
		# confirm GET /parking/available returns 2 results
		pass

	def test_retrieve_reserved(self):
		# insert into test db: 2 qvailable locs, 1 reserved locs
		# confirm GET /parking/available returns 1 result
		pass

	def test_retrieve_near(self):
		# insert into test DB: 2 points, all available, 1 mile apart
		# choose point half-mine away and test radius 0.5, 1.5, 2.5 mi
		# should return 0, 1, 2 resukts
		pass

	def test_reserve(self):
		# insert into test db: 2 qvailable locs, 1 reserved locs
		# reserve 1 loc by lat-long, check that it becomes reserved
		# reserve 1 loc by id, check that it becomes reserved
		pass

	def test_cancel(self):
		# insert into test db: 1 qvailable locs, 2 reserved locs
		# delete reservation by lat-long, check that it becomes unreserved
		# delete reservation by id, check that it becomes unreserved
		pass

	def test_cost(self):
		# insert into test db: 1 >$1 loc, 1 <$1 loc
		# ensure formatting is as expected
		pass

	def test_reserve_errors(self):
		# test that reservation with no phone returns an error
		# test reservation with invalid phone returns an error
		# test reserving pre-reserved spot returns an error
		# test reserving nonexistent slot returns an error
		pass

	def test_cancel_errors(self):
		# test cancellation with no phone returns an error
		# test cancellation with phone != existing phone returns an errir
		# test cancelling nonexistent reservation for existing plot does NOT return an error
		# test cancelling reservation on nonexistent slot returns an error
		pass

