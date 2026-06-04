from pykickoff import ProjectGenerator

# Simulate the data we'd get from the user questions
user_input = {
    "project_name": "my-cool-app",
    "description": "A weather tracking app built in Python.",
    "author_name": "Author Name",
    "author_name": "A weather tracking app built in Python.",
}

# Run the generator
gen = ProjectGenerator(user_input)
gen.run()