import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Installation',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Der Roseguarden-Server kommt mit handlichen Docker-Containern und kann daher leicht Installiert werden.
        Die Roseguarden-Hardware kann via platform.io deployed werden.
      </>
    ),
  },
  {
    title: 'Benutzerhandbuch',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Hier gibts die Infos, wie man als Admin / Benutzer auf dem Roseguarde-Server voran kommt:
        User-Accounts einrichten, RFID-Karten zuordnen und Door-Nodes installieren. Los geht`s!
      </>
    ),
  },
  {
    title: 'Entwicklerhandbuch',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Hier gibts die Entwickler-Infos, wie die Door-Nodes mit dem Server kommunizieren, wie man das Front- und Backend anpassen kann.
        It`s open source, use it!
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
