import React from 'react';
import ListStore from '../stores/List';
import '../scss/timeline.scss';

const TimelineItem = ({ data }) => (
  <div className="timeline-item">
      <div className="timeline-item-content">
        <h3>{data.title}</h3>
          <span className="tag" style={{ background: 'rgba(0,0,0,0.3)'}}>
              {data.tag_names}
          </span>
          <time>{data.created_at}</time>
          {/* <p>{data.summary}</p> */}
          <span className="circle" />
      </div>
  </div>
);

const Timeline = () =>
  ListStore.list.length > 0 && (
        <div className="timeline-container">
            {ListStore.list.map((data, idx) => (
                <TimelineItem data={data} key={idx} />
            ))}
        </div>
    );

export default Timeline