const { EufyClean } = require('eufy-clean');
const config = JSON.parse(process.argv[2]);

const eufyClean = new EufyClean(config.username, config.password);
eufyClean.init().then(() => {
    process.stdin.on('data', async (data) => {
        const command = JSON.parse(data);
        // Process command, e.g., get device status, start cleaning, etc.
        // ...
        const result = await eufyClean.getAllDevices(); // Example
        process.stdout.write(JSON.stringify(result) + '\n');
    });
});
