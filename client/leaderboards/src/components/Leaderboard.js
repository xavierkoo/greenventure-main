import React, { useState, useEffect, useRef } from "react";
import LeaderboardService from "../services/leaderboards";
import { FaCrown, FaHome } from "react-icons/fa";

const Leaderboard = () => {
	const [users, setUsers] = useState([]);
	const [mainUser, setMainUser] = useState("");
	const [userPosition, setUserPosition] = useState(0);
	const scrollingListRef = useRef(null);

	useEffect(() => {
		// Here you can fetch the data from your API or database
		LeaderboardService
			.getAll()
			.then((users) => {
				setUsers(users);
			}
		);
	}, []);

	useEffect(() => {
		if (scrollingListRef.current && userPosition >= 0) {
			const mainUserPill = scrollingListRef.current.querySelector('.glow');
			if (mainUserPill) {
				mainUserPill.scrollIntoView({ behavior: 'smooth', block: 'center' });
			}
		}
	}, [userPosition, mainUser]);
	

	// Randomize profile pictures for users
	const imageCount = 15;
	const randomizeProfilePictures = () => {
		const randInt = Math.floor(Math.random() * imageCount) + 1;
		return `${randInt}.avif`;
	}

	// Sort the users by their points
	const sortedUsers = users.sort((a, b) => b.points - a.points);

	useEffect(() => {
		window.localStorage.setItem("userID", "212814203332282"); //TODO remove
		// Get mainUser userId from local storage
		const storedMainUser = window.localStorage.getItem("userID"); //TODO check if correct way to get userID
		if (storedMainUser) {
			setMainUser(storedMainUser);
		}

		// Find the index of mainUser in sortedUsers
		const index = sortedUsers.findIndex((user) => user.userId === storedMainUser);
		setUserPosition(index)
		
	}, [sortedUsers]);

	return (
		<div>
			<div className="text-center mt-5">
				<a href="http://localhost:5173">
					<FaHome size={20}/>
				</a>
			</div>
			<div className="text-center my-5">
				<h3>Leaderboard</h3>
			</div>
			{sortedUsers.length > 0 ? (
				<>
					<div className="text-center row px-5">
						<div className="col-4 m-0 p-0">
							<div className="mb-2">
								<label><strong>2</strong></label><br/>
							</div>
							<img
								src={require(`../assets/profiles/${randomizeProfilePictures()}`)}
								alt="Profile"
								className="profile rounded-circle border border-success border-2 mb-2"
								style={{ width: "80px", height: "80px", boxShadow: "0 0 6px 2px rgba(0, 255, 0, 0.5)" }}
							/>
							<br/>
							<label><strong>@{sortedUsers[1].name}</strong></label><br/>
							<label><strong className="top-three">{sortedUsers[1].points}</strong></label>
						</div>
						<div className="text-center col-4 m-0 p-0">
							<div className="mb-2">
								<label><strong>1</strong></label><br/>
								<FaCrown size={40} color="gold"/>
							</div>
							<img
								src={require(`../assets/profiles/${randomizeProfilePictures()}`)}
								alt="Profile"
								className="profile rounded-circle border border-success border-3 mb-2"
								style={{ width: "100px", height: "100px", boxShadow: "0 0 10px 4px rgba(0, 255, 0, 0.5)" }}
							/>
							<br/>
							<label><strong>@{sortedUsers[0].name}</strong></label><br/>
							<label><strong className="top-three">{sortedUsers[0].points}</strong></label>
						</div>
						<div className="col-4 m-0 p-0">
							<div className="mb-2">
								<label><strong>3</strong></label><br/>
							</div>
							<img
								src={require(`../assets/profiles/${randomizeProfilePictures()}`)}
								alt="Profile"
								className="profile rounded-circle border border-success border-2 mb-2"
								style={{ width: "80px", height: "80px", boxShadow: "0 0 6px 2px rgba(0, 255, 0, 0.5)" }}
							/>
							<br/>
							<label><strong>@{sortedUsers[2].name}</strong></label><br/>
							<label><strong className="top-three">{sortedUsers[2].points}</strong></label>
						</div>
					</div>
					<br/>
					<div style={{ height: '475px', overflowY: 'scroll' }} ref={scrollingListRef}>
						<div className="mt-4 mx-auto">
							{sortedUsers.slice(3).map((user, index) => (
								<div className="row py-2 d-flex justify-content-center" key={user.userId}>
									<div className="col-2 d-flex justify-content-center align-items-center ps-5">
										<label><strong>{ index + 4 }</strong></label>
									</div>
									<div className="col-10">
										<div className={`badge badge-pill border border-success p-0 m-0 ${user.userId === mainUser ? 'glow' : ''}`} style={{ display: 'flex', alignItems: 'center' }}>
											<img
												src={require(`../assets/profiles/${randomizeProfilePictures()}`)}
												alt="Profile"
												className="profile rounded-circle"
												style={{ width: "50px", height: "50px" }}
											/>
											<label className="mx-5" style={{ fontSize: "12px" }}>@{user.name}</label>
											<label className="points ms-auto pe-3"><strong>{user.points}</strong></label>
										</div>
									</div>
								</div>
							))}
						</div>
					</div>
				</>
			) : (
				<p className="text-center">Loading...</p>
			)}
			<div className="blur-effect"></div>
		</div>
	);
};

export default Leaderboard;
