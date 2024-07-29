import React, { useEffect, useState } from "react";

const UsersContext = React.createContext({
  users: [], fetchUsers: () => {}
})

export default function Users() {
  const [users, setUsers] = useState([])
  const [skip, setSkip] = useState('0');
  const [limit, setLimit] = useState('100');

  const fetchUsers = async () => {
    const response = await fetch(`http://localhost:8000/users/?skip=${skip}&limit=${limit}`)
    const users = await response.json()
    console.log('users')
    console.log(users)
    setUsers(users)
    }

    /*
  useEffect(() => {
    

    if (skip && limit) {
        fetchUsers(skip, limit);
    }
    //fetchUsers()
  }, [skip, limit])
    */
  
  

  function onSkipChange(evt) {
    setSkip(evt.target.value);
  }

  function onLimitChange(evt) {
    setLimit(evt.target.value);
  }

  return (
    <UsersContext.Provider value={{users, fetchUsers}}>
        <input type="text" placeholder="Set skip" value={skip} onChange={onSkipChange} />
        <input type="text" placeholder="Set limit" value={limit} onChange={onLimitChange} />
        {/*<button type="button" onClick={e => fetchUsers(skip, limit)}>Get users</button>*/}
        <button type="button" onClick={fetchUsers}>Get users</button>
        {users?
          <div>
            <p>Skip read: {skip}, Limit read: {limit}</p>
            <p>Users:</p>
            {users.map((user) => (
           <li key={user.id}><b>{user.email}</b></li>
         ))}
         </div>
        : <div>No users</div>}
    </UsersContext.Provider>
  )
}