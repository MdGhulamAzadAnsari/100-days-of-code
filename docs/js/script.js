const projects = [
  {
    name: "Day 01",
    description: "Working with Variables in Python to Manage Data",
    link:
      "https://github.com/MdGhulamAzadAnsari/100-Days-of-Code/tree/master/Day-001",
  },
  {
    name: "Day 02",
    description: "Understanding Data Types and How to Manipulate Strings",
    link:
      "https://github.com/MdGhulamAzadAnsari/100-Days-of-Code/tree/master/Day-002",
  },
  {
    name: "Day 03",
    description: "Control Flow and Logical Operators",
    link:
      "https://github.com/MdGhulamAzadAnsari/100-Days-of-Code/tree/master/Day-003",
  },
];

const getCard = (name, description, link) => {
  var newNode = document.createElement("div");
  newNode.className = "col-xl-3 col-sm-6 col-12";
  newNode.innerHTML = `<div class="card">
                                <div class="card-body">
                                <h5 class="card-title">${name}</h5>
                                <p class="card-text">
                                ${description}
                                </p>
                                <a href="${link}" class="btn btn-primary">Source Code</a>
                                </div>
                            </div>`;
  return newNode;
};

const cardWrapper = document.getElementById("card-wrapper");

projects.forEach((project) => {
  cardWrapper.appendChild(
    getCard(project.name, project.description, project.link)
  );
});
