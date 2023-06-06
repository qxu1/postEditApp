let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {
  app.data = {
    search: '',
    users: [],
    following: {},
    add_mode: false,
    add_first_name: "",
    add_last_name: "",
    rows: [],
  };

  app.enumerate = (a) => {
    let k = 0;
    a.map((e) => {
      e._idx = k++;
    });
    return a;
  };

  app.methods = {
    follow: (user_id) => {
      axios.post(follow_url, { user_id, follow: true })
        .then(function (response) {
          let user = app.vue.users.find(user => user.id === user_id);
          if (user) {
            user.following = true;
            app.vue.following[user_id] = true;
          }
        });
    },

    unfollow: (user_id) => {
      axios.post(follow_url, { user_id: user_id, follow: false })
        .then(function (response) {
          let user = app.vue.users.find(user => user_id === user_id);
          if (user) {
            user.following = false;
            app.vue.following[user_id] = false;
          }
        });
    },

    search_users: function () {
      axios.get(get_users_url, { params: { q: this.search } }).then((result) => {
        let users = result.data.users;
        let sortedUsers = users.sort((a, b) => {
          if (this.following[a.id] && !this.following[b.id]) {
            return -1; // a comes before b
          } else if (!this.following[a.id] && this.following[b.id]) {
            return 1; // b comes before a
          } else {
            return 0; // maintain the current order
          }
        });
        this.users = app.enumerate(sortedUsers);
      });
    },

    loadUsers() {
      axios.get(get_users_url, { params: { q: this.query } })
        .then(response => {
          this.users = response.data.users;
        })
        .catch(error => {
          console.error(error);
        });
    },

    searchUsers() {
      this.loadUsers();
    },

    clear_search: function () {
      this.search = "";
      this.search_users();
    },

    add_contact: function () {
      axios.post(add_contact_url, {
        first_name: app.vue.add_first_name,
        last_name: app.vue.add_last_name,
      }).then(function (response) {
        let n = app.vue.rows.length;
        app.vue.rows.push();
        let new_row = {
          id: response.data.id,
          first_name: app.vue.add_first_name,
          last_name: app.vue.add_last_name,
          thumbnail: "",
          _state: { first_name: "clean", last_name: "clean" },
          _idx: n,
        };
        app.vue.rows.push(new_row);
        app.reset_form();
        app.set_add_status(false);
      });
    },

    reset_form: function () {
      app.vue.add_first_name = "";
      app.vue.add_last_name = "";
    },

    delete_contact: function (row_idx) {
      let id = app.vue.rows[row_idx].id;
      axios.get(delete_contact_url, { params: { id: id } }).then(function (response) {
        for (let i = 0; i < app.vue.rows.length; i++) {
          if (app.vue.rows[i].id === id) {
            app.vue.rows.splice(i, 1);
            app.enumerate(app.vue.rows);
            break;
          }
        }
      });
    },

    set_add_status: function (new_status) {
      app.vue.add_mode = new_status;
    },

    start_edit: function (row_idx, fn) {
      let row = app.vue.rows[row_idx];
      app.vue.rows[row_idx]._state[fn] = "edit";
    },

    stop_edit: function (row_idx, fn) {
      let row = app.vue.rows[row_idx];
      if (row._state[fn] === "edit") {
        row._state[fn] = "pending";
        axios.post(edit_contact_url, {
          id: row.id,
          field: fn,
          value: row[fn], // row.first_name
        }).then(function (result) {
          row._state[fn] = "clean";
        });
      }
    },

    upload_file: function (event, row_idx) {
      let input = event.target;
      let file = input.files[0];
      let row = app.vue.rows[row_idx];
      if (file) {
        let reader = new FileReader();
        reader.addEventListener("load", function () {
          axios.post(upload_thumbnail_url, {
            contact_id: row.id,
            thumbnail: reader.result,
          }).then(function () {
            row.thumbnail = reader.result;
          });
        });
        reader.readAsDataURL(file);
      }
    },
  };

  app.decorate = (a) => {
    a.map((e) => {
      e._state = { first_name: "clean", last_name: "clean" };
    });
    return a;
  };

  app.vue = new Vue({
    el: "#vue-target",
    data: app.data,
    methods: app.methods,
  });

  app.init = () => {
    axios.get(get_users_url).then(function (response) {
      app.vue.users = app.enumerate(response.data.users);
      let following = {};
      response.data.users.forEach((user) => {
        following[user.id] = user.following;
      });
      app.vue.following = following;
    });

    axios.get(load_contacts_url).then(function (response) {
      app.vue.rows = app.decorate(app.enumerate(response.data.rows));
    });
  };

  app.init();
};

init(app); // This will be the object that will contain the Vue attributes
// and be used to initialize it.

