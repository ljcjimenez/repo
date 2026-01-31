import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

// 1. Buscar la AMI más reciente de Amazon Linux 2
const ami = aws.ec2.getAmi({
    filters: [{
        name: "name",
        values: ["amzn2-ami-hvm-*-x86_64-gp2"],
    }],
    owners: ["137112412989"], // ID oficial de Amazon
    mostRecent: true,
});

// 2. Usar esa AMI en tu instancia
const server = new aws.ec2.Instance("servidor-pruebas-aws", {
    ami: ami.then(a => a.id),
    instanceType: "t2.micro",
    tags: {
        Name: "servidor-pruebas-aws",
    },
});

export const instancia_id = server.id;
export const public_ip = server.publicIp;