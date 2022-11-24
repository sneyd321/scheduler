from models.job import Job, Container, Resources

async def test_Job():
    job = Job("uuidValue")
    container = Container("image", "uuidValue")
    container.add_environment_variables("REDIS_HOST", "")
    container.add_command("python")
    container.add_command("main.py")
    container.add_command(f"--key=uuidValue")
    job.add_container(container)
    item = Resources()
    print(job.to_json())
    assert False
    
