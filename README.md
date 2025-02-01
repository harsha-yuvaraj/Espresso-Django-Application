# Espresso Blog  


**A Technology & Wellness-Centric blog** built with **Django**. Prioritizing simplicity and user experience, **Espresso** includes various features to enhance user engagement and content discovery.  

### **Check out the project live**: [www.espressoblog.online](https://www.espressoblog.online/)  



## Features  

- Tag-based filtering to focus on topics of interest.  
- **Full-text search** with stemming for ranked and accurate results. 
- Latest posts section to showcase new content.  
- Most discussed posts highlighting popular articles with high user engagement.  
- Comment system for user engagement and discussions.
- **Recommendation system** for "Similar Posts" to keep readers engaged by suggesting relevant content.   
- **Social media integration** with content sharing options for **Facebook**, **Twitter (X)**, **LinkedIn**, **Telegram**, and **Direct link sharing**.  
- **SendGrid** integration for email-based content sharing. 
- **AI** summaries of lengthy posts utilizing the **OpenAI API**.
    - **API Throttling**: Implemented **rate-limiting** with a cap of **10 requests per hour** for all users to ensure fair usage and prevent API abuse.
- **Sitemap** to enhance **SEO** and improve **search engine visibility**.
- RSS feed for easy subscription to updates. 


## Deployment  

- The application is containerized with **Docker** and the images are pushed to **AWS Elastic Container Registry (ECR)** and pulled to an **AWS EC2** instance for hosting.  
- **Nginx** is configured as a reverse proxy to route HTTP requests to the application running in the Docker container. It also handles SSL termination using certificates obtained via Certbot, ensuring the site is securely served over **HTTPS**.
- The **PostgreSQL** database is hosted on **AWS RDS** and securely connected to the EC2 instance.  
- **Terraform** is used to automate infrastructure provisioning and ensure a consistent deployment process.