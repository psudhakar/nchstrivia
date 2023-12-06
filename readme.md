1.       The tool starts with a base Spring Boot starter project that already has integrations with Vault, AWS Secrets Manager(ASM), config server with S3 and Logger configurations. 
Caveat is, the way the tool integrates with ASM, Vault and sets up Config Server may or may not work for individual projects. Few examples : 
i.         Tool is setting up a config server using spring-cloud-config-server dependency with s3 as the config backend. Haven’t seen many people using this pattern in SF. 
Teams who are deployed to K8S based platforms use ConfigMap and other platforms like ECS might use multiple different approaches including git as backend.
ii.       To integrate with ASM, tool is using AWSClientBuilder class. Teams may or may not use this approach. 
iii.     Individual project teams may or may not need Vault integration.
 
2.       Scans projects and subprojects within the WAS project, moves the Java packages to the Spring Boot project. For most part, this is a static copy, but the tool is identifying all auto generated classes (eg: wsdl2java generated classes) and does NOT copy them to the target. 
In fact, the tool is identifying some of the internal Frameworks and skipping the associated generated classes as well.

3.	Adds all the applicationContext.xml (bean configuration) files from your WAS project to Spring boot application in src/main/resources/META-INF folder. The tool recommends using Java based configuration but the tool itself does not convert xml based configuration to Java based configuration.
 
4.       Adds all WSDL files (if any) to your Spring boot application under src/main/resources/META-INF/wsdl folder, removing unnecessary Java classes
i.         Updates the pom.xml to auto generate all the required java classes to invoke a webservice.
ii.       Adds end point URLs to application YML file.
iii.     Creates a ClientConfig.java file with all the required configurations.
iv.     Adds configuration to invoke web services.
 

5.       If your app is using Db2, tool adds DB2 configurations to the Application YML file (along with all state farm db2 servers) , updates POM file with db2 dependencies, and creates DB configuration files.
If PureQuery is being used, tool advises to rewrite the db code with Spring JDBC template. The tool does not convert the code though.
 
6.       Uses a standard gitlab pipeline template for the target Spring boot project. Haven’t seen any customizations based on the project.
 
7.       Uses a standard pom.xml file for target Spring boot project but with few dynamic elements. Here are the observations:
i.         Tool only generates the dependencies for the features used in the base starter project like ASM, Config Server etc. Developer needs to copy rest of the dependencies from old pom.xml file(s) as needed
ii.       Tool adds required configuration in pom.xml to auto generate the required java classes to invoke a web service (Remember,  tool did not copy the auto generated classes from source to target)
iii.     Adds DB2 dependencies to pom file


8.       Adds SecurityConfig.java file with basic Spring Security enabled using @EnableWebSecurity with WebSecurityConfigurationAdapter. This class is now deprecated. Not recommended to use though. Teams need to update this class based on their security configuration.
